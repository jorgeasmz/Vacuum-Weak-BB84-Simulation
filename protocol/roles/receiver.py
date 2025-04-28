# -----------------------------------------------------------------------------
# File Name: receiver.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class representing the receiver in the BB84 protocol.
# -----------------------------------------------------------------------------

from .role import Role

import numpy as np

class Receiver(Role):
    """
    A Class representing the receiver in the BB84 protocol
    """    
    def __init__(self, num_bits: int):
        """
        Initialize the receiver.

        Args:
            num_bits (int): Number of bits to receive.
        """
        super().__init__('Receiver')
        self.num_bits = num_bits
        self.bases = self.random_bit_selection(num_elements=num_bits)
        self.key = np.empty(num_bits, dtype=object)
        self.states = np.empty(num_bits, dtype=object)

    def __str__(self):
        return (f"Receiver:\n"
                f"Bases: {self.bases}\n"
                f"Key: {self.measurement_results}\n")

    def perform_action(self, states):
        """
        Measure the received quantum states.

        Args:
            states (list): List of quantum states to be measured
        """
        for i, state in enumerate(states):
            self.key[i] = state.measure_state(self.bases[i])
            self.states[i] = state