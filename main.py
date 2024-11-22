from protocol import Protocol

import matplotlib.pyplot as plt

def run_multiple_simulations(nth_photon: int, num_simulations: int):
    """
    Run the protocol multiple times to collect signal and decoy yields (Y_n).

    Args:
        n_values (int): Maximum number of photons (n) to analyze (e.g., Y_1, Y_2, ...).
        num_simulations (int): Number of simulations to run.

    Returns:
        dict: Dictionary with lists of yields for each type ('signal' and 'decoy')..
    """
    expected_yields = {f'Y_{n}': [] for n in range(1, nth_photon + 1)}
    signal_yields = {f'Y_{n}': [] for n in range(1, nth_photon + 1)}
    decoy_yields = {f'Y_{n}': [] for n in range(1, nth_photon + 1)}

    for _ in range(num_simulations):
        protocol = Protocol(num_bits=1000, use_decoy_states=True, eavesdropper=False)
        protocol.run_protocol()
        for n in range(1, nth_photon + 1):
            expected_yields[f'Y_{n}'].append(protocol.expected_yields[n - 1])
            signal_yields[f'Y_{n}'].append(protocol.signal_state_yields[n - 1])
            decoy_yields[f'Y_{n}'].append(protocol.decoy_state_yields[n - 1])

    return expected_yields, signal_yields, decoy_yields

def plot_yields_boxplot(signal_yields: dict, decoy_yields: dict, expected_yields: list):
    """
    Generates a box plot for expected signal and decoy yields (Y_n).

    Args:
        signal_yields (dict): Signal yields from multiple simulations.
        decoy_yields (dict): Decoy yields from multiple simulations.
        expected_yields (list): Expected yields from multiple simulations.
    """
    data = []
    labels = []

    for n in range(1, len(expected_yields) + 1):
        data.append(expected_yields[f'Y_{n}'])
        labels.append(f'Expected Y{n}')
        data.append(signal_yields[f'Y_{n}'])
        labels.append(f'Signal Y{n}')
        data.append(decoy_yields[f'Y_{n}'])
        labels.append(f'Decoy Y{n}')

    # Create box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(data, showmeans=True, patch_artist=True)
    plt.xticks(range(1, len(labels) + 1), labels, rotation=45)
    plt.ylabel('Yield')
    plt.title('Comparison of Expected and Measured Yields (Signal and Decoy)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Número de fotones (n) y simulaciones
# nth_photon = 4
# num_simulations = 100

# Ejecutar múltiples simulaciones
# expected_yields, signal_yields, decoy_yields = run_multiple_simulations(nth_photon, num_simulations)

# Generar gráfico de cajas
# plot_yields_boxplot(signal_yields, decoy_yields, expected_yields)

protocol = Protocol(num_bits=2000, use_decoy_states=True, eavesdropper=False, mu=0.65, nu=0.08, dark_count_rate=10e-5, transmittance=0.356, signal_percentage=0.75, decoy_percentage=0.125, vacuum_percentage=0.125)

protocol.run_protocol()

print(f'Signal state gain: {protocol.signal_state_gain}')
print(f'Decoy state gain: {protocol.decoy_state_gain}')
print(f'Signal state efficiency: {protocol.signal_state_efficiency}')
print(f'Decoy state efficiency: {protocol.decoy_state_efficiency}')
print(f'Expected yields: {protocol.expected_yields}')
print(f'Signal state yields: {protocol.signal_state_yields}')
print(f'Decoy state yields: {protocol.decoy_state_yields}')
