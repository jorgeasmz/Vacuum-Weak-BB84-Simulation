# -----------------------------------------------------------------------------
# File Name: role.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class representing a role in the BB84 protocol.
# -----------------------------------------------------------------------------

from protocol.config import Config

import numpy as np

class Role:
    """
    A class representing a role in the BB84 protocol.
    """
    def __init__(self, name: str):
        self.name = name

    def perform_action(self, *args, **kwargs):
        """Perform the role's action."""
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def random_bit_selection(self, num_elements: int, seed: int = None) -> np.ndarray:
        """
        Generate an array of random bits (0s and 1s) based on a seed.
        
        Args:
            seed (int): The seed for random number generation.
            num_elements (int): The number of elements to generate.
        
        Returns:
            np.ndarray: An array of random bits (0s and 1s).
        """
        if seed is not None:
            np.random.seed(seed)
        return np.random.randint(0, 2, size=num_elements)
    
    def random_state_selection(self, num_elements: int, seed: int = None) -> np.ndarray:
        """
        Generate an array of random state types ('signal', 'decoy', 'vacuum') based on a seed.
        
        Args:
            seed (int): The seed for random number generation.
            num_elements (int): The number of elements to generate.
        
        Returns:
            np.ndarray: An array of random state types.
        """
        if seed is not None:
            np.random.seed(seed)
        
        config = Config.get_instance()
        signal_percentage = config.signal_percentage
        decoy_percentage = config.decoy_percentage
        
        # Generate random values in one operation
        rand_vals = np.random.random(num_elements)
        
        # Use vectorized operations to assign state types
        states = np.empty(num_elements, dtype=object)
        states[rand_vals < signal_percentage] = 'signal'
        states[(rand_vals >= signal_percentage) & 
               (rand_vals < signal_percentage + decoy_percentage)] = 'decoy'
        states[rand_vals >= signal_percentage + decoy_percentage] = 'vacuum'
        
        return states