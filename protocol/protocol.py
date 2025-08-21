# -----------------------------------------------------------------------------
# File Name: protocol.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class to implement the Decoy States BB84 protocol.
# -----------------------------------------------------------------------------

from .roles.sender import Sender
from .roles.receiver import Receiver
from .roles.eavesdropper import Eavesdropper
from .config import Config

import numpy as np

class Protocol:
    """
    A class to implement the Decoy States BB84 protocol.
    """
    def __init__(self, 
                 num_pulses: 1000000, 
                 eavesdropper: bool = False, 
                 attack_type: str = 'PNS',
                 mu: float = 0.65, 
                 nu: float = 0.08,  
                 alpha: float = 0.2, 
                 l: float = 20.0, 
                 channel_loss: float = 5.6,
                 receiver_loss: float = 3.5,
                 detector_efficiency: float = 0.10, 
                 detector_error_rate: float = 0.014,
                 dark_count_rate: float = 1e-5,
                 signal_percentage: float = 0.75, 
                 decoy_percentage: float = 0.125, 
                 vacuum_percentage: float = 0.125):
        """
        Initialize the protocol.
        
        Args:
            num_pulses (int): Number of pulses to be sent.
            eavesdropper (bool): Whether to include an eavesdropper.
            mu (float): Mean photon number for signal states.
            nu (float): Mean photon number for decoy states.
            alpha (float): Loss in the quantum channel in dB/km.
            channel_length (l) (float): Length of the quantum channel in km.
            channel_loss (float): Total loss in the quantum channel in dB.
            receiver_loss (float): Total loss in the receiver's side in dB.
            detector_efficiency (η_D) (float): Efficiency of the detector.
            detector_error_rate (e_d) (float): Error rate of the detector.
            dark_count_rate (Y_0)(float): Probability of dark counts (false detections).
            signal_percentage (float): Percentage of signal states.
            decoy_percentage (float): Percentage of decoy states.
            vacuum_percentage (float): Percentage of vacuum states.
        """
        # Quantum channel transmittance
        if channel_loss:
            t_AB = 10**((-channel_loss)/10)
        else:
            t_AB = 10**((-alpha * l)/10)

        t_B = 10**((-receiver_loss)/10) # Optical elements transmittance
        eta_D = detector_efficiency # Detector efficiency
        eta_Bob = t_B * eta_D # Reciever's side transmittance
        
        eta = t_AB * eta_Bob * signal_percentage # Overall transmittance
        fraction = 0.9 # Fraction of transmited pulse energy in the BS attack

        self.num_bits = num_pulses
        self.eavesdropper = eavesdropper
        self.attack_type = attack_type
        self.mu = mu
        self.nu = nu
        self.dark_count_rate = dark_count_rate
        self.transmittance = eta

        if eavesdropper and attack_type == 'BS':
            eta = eta * fraction

        # Initialize the shared configuration
        Config(mu=mu, 
               nu=nu,  
               transmittance=eta,
               detector_error_rate=detector_error_rate,
               dark_count_rate=dark_count_rate,
               signal_percentage=signal_percentage, 
               decoy_percentage=decoy_percentage, 
               vacuum_percentage=vacuum_percentage)

        self.alice = Sender(num_pulses)
        self.bob = Receiver(num_pulses)
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

        # Calculate QBER and state gain
        self.signal_state_gain = self.state_gain('signal')
        self.signal_state_qber = self.state_qber('signal')
        self.decoy_state_gain = self.state_gain('decoy')
        self.decoy_state_qber = self.state_qber('decoy')
    
    def reconcile_keys(self):
        """
        Reconcile the keys between Alice and Bob.
        """
        correct_bases = self.alice.bases == self.bob.bases
        self.reconciled_key = self.bob.key[correct_bases]

    def state_gain(self, state_type: str = 'signal'):
        """
        Calculate the state gain for a specific state type ('signal' or 'decoy').
        
        State gain is the ratio of detected pulses to the number of pulses with matching bases.

        Args:
            state_type (str): The type of state to calculate gain for.

        Returns:
            float: The calculated gain for the specified state type.
        """
        # Find indices of pulses with the specified state type
        state_indices = np.where(self.alice.states_types == state_type)[0]
        
        # Filter for pulses where bases match
        matching_bases_indices = [i for i in state_indices if self.alice.bases[i] == self.bob.bases[i]]
        total_matching_pulses = len(matching_bases_indices)
        
        if total_matching_pulses == 0:
            return 0
            
        # Count valid detections
        detections = 0
        for i in matching_bases_indices:
            if self.bob.key[i] != 'No detection':
                detections += 1
                
        return detections / total_matching_pulses

    def state_qber(self, state_type: str = 'signal'):
        """
        Calculate the Quantum Bit Error Rate (QBER) for a specific state type.
        
        QBER is the ratio of incorrect bits to the total number of detected bits
        where bases match.

        Args:
            state_type (str): The type of state to calculate QBER for.

        Returns:
            float: The calculated QBER for the specified state type.
        """
        # Find indices of pulses with the specified state type and matching bases
        state_indices = np.where(self.alice.states_types == state_type)[0]
        matching_bases_indices = [i for i in state_indices if self.alice.bases[i] == self.bob.bases[i]]
        
        # Count detections and errors
        detections = 0
        errors = 0
        for i in matching_bases_indices:
            if self.bob.key[i] != 'No detection':
                detections += 1
                if self.alice.key[i] != self.bob.key[i]:
                    errors += 1
                    
        # Avoid division by zero
        if detections == 0:
            return 0
                    
        return errors / detections