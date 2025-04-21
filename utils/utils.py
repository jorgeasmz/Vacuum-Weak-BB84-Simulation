def print_protocol_results(protocol):
    """
    Prints the results of a protocol run.
    
    Args:
        protocol (Protocol): Protocol instance after execution.
    """
    print(f'Signal state gain: {protocol.signal_state_gain}')
    print(f'Decoy state gain: {protocol.decoy_state_gain}')
    print(f'Signal state efficiency: {protocol.signal_state_efficiency}')
    print(f'Decoy state efficiency: {protocol.decoy_state_efficiency}')
    print(f'Expected yields: {protocol.expected_yields}')
    print(f'Signal state yields: {protocol.signal_state_yields}')
    print(f'Decoy state yields: {protocol.decoy_state_yields}')

def convert_single_run_to_dict(protocol, nth_photon, protocol_params):
    """
    Converts single run results to dictionary format for saving.
    
    Args:
        protocol (Protocol): Protocol instance after execution.
        nth_photon (int): Maximum number of photons to consider.
        protocol_params (dict): Original parameters used to create the protocol.
    
    Returns:
        tuple: (expected_yields, signal_yields, decoy_yields, protocol_params)
    """
    # Convert data to dictionaries for persistence
    expected_yields = {f'Y_{n}': [protocol.expected_yields[n-1]] for n in range(1, nth_photon + 1)}
    signal_yields = {f'Y_{n}': [protocol.signal_state_yields[n-1]] for n in range(1, nth_photon + 1)}
    decoy_yields = {f'Y_{n}': [protocol.decoy_state_yields[n-1]] for n in range(1, nth_photon + 1)}
    
    return expected_yields, signal_yields, decoy_yields, protocol_params

def print_saved_results(expected_yields, signal_yields, decoy_yields, params):
    """
    Prints the results loaded from a saved file.
    
    Args:
        expected_yields (dict): Expected yields dictionary.
        signal_yields (dict): Signal yields dictionary.
        decoy_yields (dict): Decoy yields dictionary.
        params (dict): Protocol parameters used.
    """
    print("\n--- Saved Protocol Results ---")
    
    # Extract the first values for single run results
    if all(len(expected_yields[key]) == 1 for key in expected_yields):
        expected = [expected_yields[f'Y_{n}'][0] for n in range(1, len(expected_yields) + 1)]
        signal = [signal_yields[f'Y_{n}'][0] for n in range(1, len(signal_yields) + 1)]
        decoy = [decoy_yields[f'Y_{n}'][0] for n in range(1, len(decoy_yields) + 1)]
        
        # Print main results if available in parameters
        if 'signal_state_gain' in params:
            print(f'Signal state gain: {params["signal_state_gain"]}')
        if 'decoy_state_gain' in params:
            print(f'Decoy state gain: {params["decoy_state_gain"]}')
        if 'signal_state_efficiency' in params:
            print(f'Signal state efficiency: {params["signal_state_efficiency"]}')
        if 'decoy_state_efficiency' in params:
            print(f'Decoy state efficiency: {params["decoy_state_efficiency"]}')
        
        # Print yields
        print(f'Expected yields: {expected}')
        print(f'Signal state yields: {signal}')
        print(f'Decoy state yields: {decoy}')
    else:
        # For multiple runs, print summary statistics
        print("Summary statistics for multiple runs:")
        for n in range(1, len(expected_yields) + 1):
            print(f"\n--- Photon number {n} ---")
            print(f"Expected Y_{n}: mean={sum(expected_yields[f'Y_{n}'])/len(expected_yields[f'Y_{n}']):.6f}")
            print(f"Signal Y_{n}: mean={sum(signal_yields[f'Y_{n}'])/len(signal_yields[f'Y_{n}']):.6f}")
            print(f"Decoy Y_{n}: mean={sum(decoy_yields[f'Y_{n}'])/len(decoy_yields[f'Y_{n}']):.6f}")

def get_protocol_parameters():
    """
    Prompts the user for protocol parameters.
    
    Returns:
        dict: Dictionary with all protocol parameters.
    """
    # Ask for required parameters
    num_bits = int(input("Number of bits: "))
    use_decoy_states = input("Use decoy states? (y/n): ").lower() == 'y'
    eavesdropper = input("Include eavesdropper? (y/n): ").lower() == 'y'
    
    # Default values
    default_params = {
        'num_bits': num_bits,
        'use_decoy_states': use_decoy_states,
        'eavesdropper': eavesdropper,
        'mu': 0.65,
        'nu': 0.08,
        'dark_count_rate': 10e-5,
        'channel_loss': 5.6,
        'channel_length': 20.0,
        'receiver_loss': 3.5,
        'detection_efficiency': 0.10,
        'signal_percentage': 0.75,
        'decoy_percentage': 0.125,
        'vacuum_percentage': 0.125
    }
    
    # Ask if default parameters should be used
    use_defaults = input("Use default parameters for the rest? (y/n): ").lower() == 'y'
    
    # If not using defaults, ask for each parameter
    if not use_defaults:
        default_params['mu'] = float(input("Signal state intensity (mu): "))
        default_params['nu'] = float(input("Decoy state intensity (nu): "))
        default_params['dark_count_rate'] = float(input("Dark count rate: "))
        default_params['channel_loss'] = float(input("Channel loss (dB): "))
        default_params['channel_length'] = float(input("Channel length (km): "))
        default_params['receiver_loss'] = float(input("Receiver loss (dB): "))
        default_params['detection_efficiency'] = float(input("Detection efficiency: "))
        default_params['signal_percentage'] = float(input("Signal state percentage: "))
        default_params['decoy_percentage'] = float(input("Decoy state percentage: "))
        default_params['vacuum_percentage'] = float(input("Vacuum state percentage: "))
    
    return default_params