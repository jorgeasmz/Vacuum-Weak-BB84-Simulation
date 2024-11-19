

class Config:
    _instance = None

    def __new__(cls, mu=None, nu=None, dark_count_rate=None):
        
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.mu = mu
            cls._instance.nu = nu
            cls._instance.dark_count_rate = dark_count_rate
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    @staticmethod
    def state_type_to_mean_photon_number(state_type: str) -> float:
        """
        Convert state type to mean photon number.
        
        Args:
            state_type (str): The type of the state ('signal', 'decoy', 'vacuum')
        
        Returns:
            float: The mean photon number for the given state type.
        """
        config = Config.get_instance()
        if state_type == 'signal':
            return config.mu
        elif state_type == 'decoy':
            return config.nu
        elif state_type == 'vacuum':
            return config.dark_count_rate
        else:
            raise ValueError("Invalid state type")