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
    
    
    def random_selection(self, num_elements: int, seed: int = None) -> list:
        """
        Generate a list of random values based on a seed.
        
        Args:
            seed (int): The seed for random number generation.
            num_elements (int): The number of elements to generate.
        
        Returns:
            list: A list of random values.
        """
       
        random.seed(seed)

        if seed is not None and seed > 50:
            # Generate a list of intensity types
            return [
                'signal' if random.random() < 0.875 else 
                'decoy' if random.random() < 0.9375 else 
                'vacuum' for _ in range(num_elements)
            ]
        
        else:
            # Generate a list of 0s and 1s
            return [random.choice([0, 1]) for _ in range(num_elements)]