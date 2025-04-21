# -----------------------------------------------------------------------------
# File Name: role.py
# Author: jorgeasmz
# Date: 21/11/2024
# Description: A class representing a role in the BB84 protocol.
# -----------------------------------------------------------------------------

from protocol.config import Config

import random

class Role:
    """
    A class representing a role in the BB84 protocol.
    """
    def __init__(self, name: str):
        self.name = name

    def perform_action(self, *args, **kwargs):
        """Perform the role's action."""
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def random_bit_selection(self, num_elements: int, seed: int = None) -> list:
        """
        Generate a list of random bits (0s and 1s) based on a seed.
        
        Args:
            seed (int): The seed for random number generation.
            num_elements (int): The number of elements to generate.
        
        Returns:
            list: A list of random bits (0s and 1s).
        """
        random.seed(seed)
        return [random.choice([0, 1]) for _ in range(num_elements)]
    
    def random_state_selection(self, num_elements: int, seed: int = None) -> list:
        """
        Generate a list of random state types ('signal', 'decoy', 'vacuum') based on a seed.
        
        Args:
            seed (int): The seed for random number generation.
            num_elements (int): The number of elements to generate.
        
        Returns:
            list: A list of random state types.
        """
        random.seed(seed)
        
        config = Config.get_instance()
        signal_percentage = config.signal_percentage
        decoy_percentage = config.decoy_percentage

        states_types = []
        for _ in range(num_elements):
            rand_val = random.random()
            if rand_val < signal_percentage:
                states_types.append('signal')
            elif rand_val < signal_percentage + decoy_percentage:
                states_types.append('decoy')
            else:
                states_types.append('vacuum')
        
        return states_types