from protocol.protocol import Protocol

def run_multiple_simulations(nth_photon: int, num_simulations: int, protocol_params: dict):
    """
    Run the protocol multiple times to collect signal and decoy yields (Y_n).

    Args:
        nth_photon (int): Maximum number of photons (n) to analyze (e.g., Y_1, Y_2, ...).
        num_simulations (int): Number of simulations to run.
        protocol_params (dict): Parameters for protocol configuration.

    Returns:
        tuple: Dictionary with lists of yields for each type (expected, signal and decoy).
    """
    expected_yields = {f'Y_{n}': [] for n in range(1, nth_photon + 1)}
    signal_yields = {f'Y_{n}': [] for n in range(1, nth_photon + 1)}
    decoy_yields = {f'Y_{n}': [] for n in range(1, nth_photon + 1)}

    for _ in range(num_simulations):
        # Create protocol with provided parameters
        protocol = Protocol(num_bits=protocol_params['num_bits'], 
                            use_decoy_states=protocol_params['use_decoy_states'], 
                            eavesdropper=protocol_params['eavesdropper'], 
                            mu=protocol_params['mu'], 
                            nu=protocol_params['nu'], 
                            dark_count_rate=protocol_params['dark_count_rate'],
                            channel_loss=protocol_params['channel_loss'],
                            channel_length=protocol_params['channel_length'],
                            receiver_loss=protocol_params['receiver_loss'],
                            detection_efficiency=protocol_params['detection_efficiency'],                            
                            signal_percentage=protocol_params['signal_percentage'], 
                            decoy_percentage=protocol_params['decoy_percentage'], 
                            vacuum_percentage=protocol_params['vacuum_percentage'])
        
        protocol.run_protocol()

        for n in range(1, nth_photon + 1):
            expected_yields[f'Y_{n}'].append(protocol.expected_yields[n - 1])
            signal_yields[f'Y_{n}'].append(protocol.signal_state_yields[n - 1])
            decoy_yields[f'Y_{n}'].append(protocol.decoy_state_yields[n - 1])

    return expected_yields, signal_yields, decoy_yields