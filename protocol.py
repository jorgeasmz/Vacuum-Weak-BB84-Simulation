from roles.sender import Sender
from roles.receiver import Receiver
from roles.eavesdropper import Eavesdropper

import numpy as np

class Protocol:
    """
    A class to implement the BB84 and Decoy States BB84 protocols.
    """
    
    def __init__(self, num_bits: int, use_decoy_states: bool = False, 
                 eavesdropper: bool = False, mu: float = 0.5, nu: float = 0.1, 
                 dark_count_rate: float = 10e-5, transmittance: float = 10e-3):
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
        """
        self.num_bits = num_bits
        self.use_decoy_states = use_decoy_states
        self.eavesdropper = eavesdropper
        self.mu = mu
        self.nu = nu
        self.dark_count_rate = dark_count_rate
        self.transmittance = transmittance
        self.alice = Sender(num_bits, mu, nu, dark_count_rate, use_decoy_states)
        self.bob = Receiver(num_bits)
        self.eve = Eavesdropper() if eavesdropper else None

    def run_protocol(self):
        """
        Run the BB84 protocol.
        """
        # Alice generates quantum states
        states = self.alice.perform_action()
        
        # If Eve is present, intercept the states
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

    def state_gain(self, intensity_type: str = 'signal'):
        """
        Calculate the state gain for a specific intensity type ('signal', 'decoy', or 'vacuum').

        Args:
            intensity_type (str): The type of intensity to calculate gain for.

        Returns:
            float: The calculated gain for the specified intensity type.
        """
        # Obtain the indices of the states corresponding to the specified intensity type.
        state_indices = [i for i, t in enumerate(self.alice.intensity_types) if t == intensity_type]
        
        # Counting the total pulses of this type of condition
        total_state_pulses = len(state_indices)

        print("Total state pulses:", total_state_pulses)
        
        # Count the detections in those specific indexes of 'measurement_results'.
        detections = sum(1 for i in state_indices if self.bob.measurement_results[i] != 'No detection')

        print("Detections:", detections)
        
        # Calculate the gain as the fraction of detections
        return detections / total_state_pulses if total_state_pulses > 0 else 0
    
    def state_efficiency(self, state_gain: float, intensity_type: str = 'signal'):
        """
        Calculate the state efficiency for a specific intensity type ('signal', 'decoy', 'vaccum').

        Args:
            intensity_type (str): The type of intensity to calculate efficiency for.

        Returns:
            float: The calculated efficiency for the specified intensity type.
        """
        
        # Needed parameters
        Y_0 = self.dark_count_rate
        Q = state_gain
        mean_photon_number = self.alice.intensity_type_to_mean_photon_number(intensity_type)

        # Calculate efficiency
        efficiency = -np.log(np.abs(1 + Y_0 - Q)) / mean_photon_number
        
        return efficiency
    
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
        # Calculate the expected photon number dependent yields
        expected_yields = [self.n_photon_state_yield(self.transmittance, n) for n in range(5)]

        # Measured signal state gain
        signal_state_gain = self.state_gain('signal')

        # Calculate signal state efficiency
        signal_state_efficiency = self.state_efficiency(signal_state_gain, 'signal')

        # Calculate the signal state photon number dependent yields
        signal_state_yields = [self.n_photon_state_yield(signal_state_efficiency, n) for n in range(5)]

        # Measured decoy state gain
        decoy_state_gain = self.state_gain('decoy')

        # Calculate decoy state efficiency
        decoy_state_efficiency = self.state_efficiency(decoy_state_gain, 'decoy')

        # Calculate the decoy state photon number dependent yields
        decoy_state_yields = [self.n_photon_state_yield(decoy_state_efficiency, n) for n in range(5)]

        print("Expected yields:", expected_yields)
        print("Signal state yields:", signal_state_yields)
        print("Decoy state yields:", decoy_state_yields)


    
