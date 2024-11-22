# -----------------------------------------------------------------------------
# File Name: protocol.py
# Author: jorgeasmz
# Date: 21/11/2024
# Description: A class to implement the Decoy States BB84 protocol.
# -----------------------------------------------------------------------------

from roles.sender import Sender
from roles.receiver import Receiver
from roles.eavesdropper import Eavesdropper
from config import Config

import numpy as np

class Protocol:
    """
    A class to implement the Decoy States BB84 protocol.
    """
    def __init__(self, num_bits: int, use_decoy_states: bool = False, 
                 eavesdropper: bool = False, mu: float = 0.5, nu: float = 0.1, 
                 dark_count_rate: float = 10e-5, transmittance: float = 10e-3,
                 signal_percentage: float = 0.875, decoy_percentage: float = 0.0625, 
                 vacuum_percentage: float = 0.0625):
        """
        Initialize the protocol.
        
        Args:
            num_bits (int): Number of bits to be transmitted.
            use_decoy_states (bool): Whether to use decoy states.
            eavesdropper (bool): Whether to include an eavesdropper.
            mu (float): Mean photon number for signal states.
            nu (float): Mean photon number for decoy states.
            dark_count_rate (float): Probability of dark counts (false detections).
            transmittance (float): The transmittance of the quantum channel.
            signal_percentage (float): Percentage of signal states.
            decoy_percentage (float): Percentage of decoy states.
            vacuum_percentage (float): Percentage of vacuum states.
        """
        self.num_bits = num_bits
        self.use_decoy_states = use_decoy_states
        self.eavesdropper = eavesdropper
        self.mu = mu
        self.nu = nu
        self.dark_count_rate = dark_count_rate
        self.transmittance = transmittance

        # Initialize the shared configuration
        Config(mu=mu, nu=nu, dark_count_rate=dark_count_rate, signal_percentage=signal_percentage, decoy_percentage=decoy_percentage, vacuum_percentage=vacuum_percentage)

        self.alice = Sender(num_bits, use_decoy_states)
        self.bob = Receiver(num_bits)
        self.eve = Eavesdropper() if eavesdropper else None

    def run_protocol(self):
        """
        Run the BB84 protocol.
        """
        # Alice generates quantum states
        states = self.alice.perform_action()
        
        # If Eve is present, intercepts the states
        if self.eavesdropper:
            states = self.eve.perform_action(states)
                    
        # Bob measures the states
        self.bob.perform_action(states)
        
        # Reconcile keys
        self.reconcile_keys()

        # Detect eavesdropper
        self.detect_eavesdropper()
    
    def reconcile_keys(self):
        """
        Reconcile the keys between Alice and Bob.
        """
        reconciled_key = []
        for i in range(self.num_bits):
            if self.alice.bases[i] == self.bob.bases[i]:
                reconciled_key.append(self.bob.measurement_results[i])
        self.reconciled_key = reconciled_key

    def state_gain(self, state_type: str = 'signal'):
        """
        Calculate the state gain for a specific state tpye ('signal', 'decoy', or 'vacuum').

        Args:
            state_type (str): The type of state to calculate gain for.

        Returns:
            float: The calculated gain for the specified state type.
        """
        state_indices = [i for i, t in enumerate(self.alice.states_types) if t == state_type]
        total_state_pulses = len(state_indices)
        print(f'Total state pulses: {total_state_pulses}')
        detections = sum(1 for i in state_indices if self.bob.measurement_results[i] != 'No detection' and self.alice.bases[i] == self.bob.bases[i])
        print(f'Detections: {detections}')

        return detections / total_state_pulses if total_state_pulses > 0 else 0
    
    def state_efficiency(self, state_gain: float, state_type: str = 'signal'):
        """
        Calculate the state efficiency for a specific state type ('signal', 'decoy', 'vaccum').

        Args:
            state_type (str): The type of state to calculate efficiency for.

        Returns:
            float: The calculated efficiency for the specified state type.
        """

        Y_0 = self.dark_count_rate
        Q = state_gain
        mean_photon_number = Config.state_type_to_mean_photon_number(state_type)
        
        return -np.log(np.abs(1 + Y_0 - Q)) / mean_photon_number
    
    def n_photon_state_yield(self, state_efficiency, n):
        """
        Calculate the yield of n-photon states.

        Args:
            state_efficiency (float): The efficiency of the state.
            n (int): The number of photons in the state.

        Returns:
            float: The calculated yield of n-photon states.
        """
        return self.dark_count_rate + (1 - (1 - state_efficiency)**n)
    
    def detect_eavesdropper(self):
        """
        Detect the presence of an eavesdropper.
        """
        self.expected_yields = [self.n_photon_state_yield(self.transmittance, n) for n in range(1, 5)]

        self.signal_state_gain = self.state_gain('signal')
        self.signal_state_efficiency = self.state_efficiency(self.signal_state_gain, 'signal')
        self.signal_state_yields = [self.n_photon_state_yield(self.signal_state_efficiency, n) for n in range(1, 5)]

        self.decoy_state_gain = self.state_gain('decoy')
        self.decoy_state_efficiency = self.state_efficiency(self.decoy_state_gain, 'decoy')
        self.decoy_state_yields = [self.n_photon_state_yield(self.decoy_state_efficiency, n) for n in range(1, 5)]
