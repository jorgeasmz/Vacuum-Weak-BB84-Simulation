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
        return [
            'signal' if random.random() < 0.875 else 
            'decoy' if random.random() < 0.9375 else 
            'vacuum' for _ in range(num_elements)
        ]