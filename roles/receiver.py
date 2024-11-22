# -----------------------------------------------------------------------------
# File Name: receiver.py
# Author: jorgeasmz
# Date: 21/11/2024
# Description: A class representing the receiver in the BB84 protocol.
# -----------------------------------------------------------------------------

from .role import Role

class Receiver(Role):
    """
    A Class representing the receiver in the BB84 protocol
    """    
    def __init__(self, num_bits: int):
        """
        Initialize the receiver.

        Args:
            num_bits (int): Number of bits to be transmitted.
        """
        super().__init__('Receiver')
        self.bases = self.random_bit_selection(num_elements=num_bits)
        self.measurement_results = []
        self.states = []

    def __str__(self):
        return (f"Receiver:\n"
                f"Bases: {self.bases}\n"
                f"Measurement results: {self.measurement_results}\n")

    def perform_action(self, states):
        """
        Measure the received quantum states.

        Args:
            states (list): List of quantum states to be measured
        """
        i = 0
        for state in states:
            result = state.measure_state(self.bases[i])
            self.measurement_results.append(result if result is not None else 'No detection')
            self.states.append(states)
            i += 1
            