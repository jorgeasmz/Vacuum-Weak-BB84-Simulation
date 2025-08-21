import numpy as np
import json
import os

from protocol.protocol import Protocol
from tqdm import tqdm

def eta_state(mpn: float, state_gain: float, dark_count_rate: float) -> float:
    """
    Calculate the state efficiency for a specific state type ('signal' or 'decoy').

    Args:
        mpn (float): Mean photon number.
        state_gain (float): The gain of the state.
        dark_count_rate (float): The dark count rate.

    Returns:
        float: The calculated efficiency for the specified state type.
    """
    return -np.log(np.abs(1 + dark_count_rate - state_gain)) / mpn

def yield_i(n: int, eta_state: float, dark_count_rate: float) -> float:
    """
    Calculate the yield of n-photon states.

    Args:
        n (int): The number of photons in the state.
        eta_state (float): The efficiency of the state.
        dark_count_rate (float): The dark count rate.

    Returns:
        float: The calculated yield of n-photon states.
    """
    return dark_count_rate + (1 - (1 - eta_state)**n)

def generate_filename(num_runs, num_pulses, attack_type):
    """
    Generate a filename with the specified format.
    
    Args:
        num_runs: Number of simulation runs
        num_pulses: Number of pulses in the sequence
        attack_type: Type of attack used ("PNS", "BS", or "No-Eve")
        
    Returns:
        String with the generated filename
    """
    return f"Runs_{num_runs}_Length_{num_pulses}_{attack_type}.json"

def save_yields_to_file(y_expected, y_signal, y_decoy, n_values, num_runs, num_pulses, 
                        attack_type, mu, nu, alpha, l, channel_loss, receiver_loss, 
                        detector_efficiency, detector_error_rate, dark_count_rate,
                        signal_percentage, decoy_percentage, vacuum_percentage,
                        eta, signal_state_gain, decoy_state_gain):
    """
    Save yield data to a JSON file with specified format.
    
    Args:
        y_expected: List of lists with expected yields
        y_signal: List of lists with signal yields
        y_decoy: List of lists with decoy yields
        n_values: n values used
        num_runs: Number of simulation runs
        num_pulses: Number of pulses in the sequence
        [Additional simulation parameters]
        attack_type: "PNS", "BS", or "No-Eve"
    """
    # Create results directory if it doesn't exist
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"Created directory: {results_dir}")
    
    data = {
        'simulation_params': {
            'num_runs': num_runs,
            'num_pulses': num_pulses,
            'attack_type': attack_type,
            'mu': mu,
            'nu': nu,
            'alpha': alpha,
            'l': l,
            'channel_loss': channel_loss,
            'receiver_loss': receiver_loss,
            'detector_efficiency': detector_efficiency,
            'detector_error_rate': detector_error_rate,
            'dark_count_rate': dark_count_rate,
            'signal_percentage': signal_percentage,
            'decoy_percentage': decoy_percentage,
            'vacuum_percentage': vacuum_percentage,
            'eta': eta,
            'signal_state_gain': signal_state_gain,
            'decoy_state_gain': decoy_state_gain
        },
        'n_values': n_values,
        'y_expected': [list(map(float, yields)) for yields in y_expected],
        'y_signal': [list(map(float, yields)) for yields in y_signal],
        'y_decoy': [list(map(float, yields)) for yields in y_decoy]
    }
    
    filename = generate_filename(num_runs, num_pulses, attack_type)
    filepath = os.path.join(results_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to '{filepath}'")
    return filepath

def main():
    """Main function to run the BB84 QKD simulation"""
    
    # Fixed simulation parameters
    num_runs = 5
    num_pulses = 100
    mu = 0.65
    nu = 0.08
    alpha = 0.2
    l = 20.0
    channel_loss = 5.6
    receiver_loss = 3.5
    detector_efficiency = 0.10
    detector_error_rate = 0.014
    dark_count_rate = 1e-5
    signal_percentage = 0.75
    decoy_percentage = 0.125
    vacuum_percentage = 0.125

    # Eavesdropper settings - Choose one: "No-Eve", "PNS", or "BS"
    attack_type = "No-Eve"  # Change this to "BS" or "No-Eve" as needed
    eavesdropper = attack_type != "No-Eve"

    # Values of n for the yield calculation
    n_values = list(range(1, 6))

    # Yield lists for expected, signal, and decoy states
    y_expected = [[] for _ in n_values]
    y_signal = [[] for _ in n_values]
    y_decoy = [[] for _ in n_values]

    for run in tqdm(range(num_runs), desc="Simulations", unit="sim"):

        # Execute the protocol
        protocol = Protocol(
                  num_pulses=num_pulses,
                  eavesdropper=eavesdropper,
                  attack_type=attack_type,
                  mu=mu,
                  nu=nu,
                  alpha=alpha,
                  l=l,
                  channel_loss=channel_loss,
                  receiver_loss=receiver_loss,
                  detector_efficiency=detector_efficiency,
                  detector_error_rate=detector_error_rate,
                  dark_count_rate=dark_count_rate,
                  signal_percentage=signal_percentage,
                  decoy_percentage=decoy_percentage,
                  vacuum_percentage=vacuum_percentage
        )

        protocol.run_protocol()
        
        eta = protocol.transmittance
        dark_count_rate = protocol.dark_count_rate

        # Calculate the state efficiency for signal and decoy states
        eta_signal = eta_state(protocol.mu, protocol.signal_state_gain, dark_count_rate)
        eta_decoy = eta_state(protocol.nu, protocol.decoy_state_gain, dark_count_rate)
        
        # Calculate yields for each n value
        for i, n in enumerate(n_values):
            y_expected[i].append(yield_i(n, eta, dark_count_rate))
            y_signal[i].append(yield_i(n, eta_signal, dark_count_rate))
            y_decoy[i].append(yield_i(n, eta_decoy, dark_count_rate))
    
    # Save data to a file
    filepath = save_yields_to_file(
        y_expected, y_signal, y_decoy, n_values, num_runs, num_pulses,
        attack_type, mu, nu, alpha, l, channel_loss, receiver_loss,
        detector_efficiency, detector_error_rate, dark_count_rate,
        signal_percentage, decoy_percentage, vacuum_percentage,
        eta, protocol.signal_state_gain, protocol.decoy_state_gain
    )
    
    print(f"Simulation completed. Run 'python visualization.py --file {os.path.basename(filepath)}' to generate the plot.")

if __name__ == "__main__":
    main()