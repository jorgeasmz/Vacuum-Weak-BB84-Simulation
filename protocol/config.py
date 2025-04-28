# -----------------------------------------------------------------------------
# File Name: config.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class to store the configuration of the protocol.
# -----------------------------------------------------------------------------

class Config:
    _instance = None

    def __new__(cls, 
                mu=None, 
                nu=None, 
                transmittance=None,
                detector_error_rate=None,
                dark_count_rate=None,
                signal_percentage=None, 
                decoy_percentage=None, 
                vacuum_percentage=None):
        
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.mu = mu
            cls._instance.nu = nu
            cls._instance.transmittance = transmittance
            cls._instance.detector_error_rate = detector_error_rate
            cls._instance.dark_count_rate = dark_count_rate
            cls._instance.signal_percentage = signal_percentage
            cls._instance.decoy_percentage = decoy_percentage
            cls._instance.vacuum_percentage = vacuum_percentage

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
            return 0
        else:
            raise ValueError("Invalid state type")