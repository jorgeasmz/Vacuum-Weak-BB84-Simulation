

from .role import Role
from state import State

class Sender(Role):
    """
    A class representing the sender in the BB84 protocol.
    """    
    def __init__(self, num_bits: int, mu: float, nu: float, 
                 dark_count_rate: float, use_decoy_states: bool = False):
        """
        Initialize the sender.
        
        Args:
            num_bits (int): Number of bits to be transmitted.
            mu (float): Mean photon number for signal states.
            nu (float): Mean photon number for decoy states.
            dark_count_rate (float): Probability of dark counts (false detections).
            use_decoy_states (bool): Whether to use decoy states.
        """
        super().__init__('Sender')
        self.num_bits = num_bits
        self.use_decoy_states = use_decoy_states
        self.mu = mu
        self.nu = nu
        self.dark_count_rate = dark_count_rate
        self.states = []
        self.bases = self.random_selection(num_elements=num_bits, seed=12)
        self.original_key = self.random_selection(num_elements=num_bits, seed=14)
        self.intensity_types = self.random_selection(num_elements=num_bits, seed=52) if use_decoy_states else ['signal'] * num_bits

    def __str__(self):
        return (f"Sender:\n"
                f"Number of bits: {self.num_bits}\n"
                f"Use decoy states: {self.use_decoy_states}\n"
                f"Bases: {self.bases}\n"
                f"Original key: {self.original_key}\n")
    
    def intensity_type_to_mean_photon_number(self, intensity_type: str):
        """
        Map an intensity type to the corresponding mean photon number.

        Args:
            intensity_type (str): The type of intensity to map.

        Returns:
            float: The mean photon number corresponding to the specified intensity type.
        """
        if intensity_type == 'signal':
            return self.mu
        elif intensity_type == 'decoy':
            return self.nu
        else:
            return self.dark_count_rate

    def perform_action(self):
        """
        Generate quantum states for the protocol.

        Returns:
            list[State]: A list of quantum states.
        """
        for i in range(self.num_bits):
            mean_photon_number = self.intensity_type_to_mean_photon_number(self.intensity_types[i])
            state = State(self.original_key[i], self.bases[i], mean_photon_number)
            self.states.append(state)
        return self.states