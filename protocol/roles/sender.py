# -----------------------------------------------------------------------------
# File Name: sender.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class representing the sender in the BB84 protocol.
# -----------------------------------------------------------------------------

from .role import Role
from protocol.state import State

import numpy as np

class Sender(Role):
    """
    A class representing the sender in the BB84 protocol.
    """    
    def __init__(self, num_bits: int):
        """
        Initialize the sender.
        
        Args:
            num_bits (int): Number of bits to be transmitted.
        """
        super().__init__('Sender')
        self.num_bits = num_bits
        self.key = self.random_bit_selection(num_elements=num_bits)
        self.bases = self.random_bit_selection(num_elements=num_bits)
        self.states_types = self.random_state_selection(num_elements=num_bits)
        self.states = np.empty(num_bits, dtype=object)

    def __str__(self):
        return (f"Sender:\n"
                f"Number of bits: {self.num_bits}\n"
                f"Key: {self.sender_key}\n"
                f"Bases: {self.bases}\n")

    def perform_action(self):
        """
        Generate quantum states for the protocol.

        Returns:
            np.ndarray: An array of quantum states.
        """
        for i in range(self.num_bits):
            self.states[i] = State(self.key[i], self.bases[i], self.states_types[i])
            
        return self.states