

from .role import Role
from state import State

class Sender(Role):
    """
    A class representing the sender in the BB84 protocol.
    """    
    def __init__(self, num_bits: int, use_decoy_states: bool):
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
        self.states = []
        self.bases = self.random_bit_selection(num_elements=num_bits)
        self.original_key = self.random_bit_selection(num_elements=num_bits)
        self.states_types = self.random_state_selection(num_elements=num_bits) if use_decoy_states else ['signal'] * num_bits

    def __str__(self):
        return (f"Sender:\n"
                f"Number of bits: {self.num_bits}\n"
                f"Use decoy states: {self.use_decoy_states}\n"
                f"Bases: {self.bases}\n"
                f"Original key: {self.original_key}\n")

    def perform_action(self):
        """
        Generate quantum states for the protocol.

        Returns:
            list[State]: A list of quantum states.
        """
        for i in range(self.num_bits):
            state = State(self.original_key[i], self.bases[i], self.states_types[i])
            self.states.append(state)
        return self.states