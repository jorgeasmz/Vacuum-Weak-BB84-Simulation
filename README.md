# Vacuum-Weak BB84 Quantum Key Distribution Protocol Simulation

## Overview
This project implements a simulation of the BB84 Quantum Key Distribution (QKD) protocol with decoy states, focusing on vacuum-weak coherent pulse implementations. The BB84 protocol is a quantum cryptographic protocol that allows two parties to securely share a secret key. This implementation includes simulation of photon-number splitting attacks and beam splitter attacks, with yield analysis capabilities for security assessment.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Technologies](#technologies)
7. [License](#license)

## Features
- **Vacuum-Weak Coherent Pulse Simulation**: Implements realistic quantum state preparation with coherent pulses
- **Decoy States**: Signal, decoy, and vacuum states for enhanced security against photon number splitting attacks
- **Attack Simulation**: Supports photon number splitting (PNS) and beam splitter (BS) attacks
- **Yield Analysis**: Calculates and analyzes n-photon yields for security assessment
- **Multiple Simulations**: Run multiple protocol executions for statistical analysis
- **Data Persistence**: Save simulation results in JSON format for later analysis
- **Visualization Tools**: Generate LaTeX-formatted plots for yield analysis
- **Parameter Customization**: Configure protocol parameters including mean photon numbers, losses, and detector characteristics

## Installation
### Prerequisites
- Python 3.8+
- Required Python packages (see requirements.txt):
  - qiskit
  - qiskit-aer
  - matplotlib
  - numpy
  - tqdm

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/jorgeasmz/Vacuum-Weak-BB84-Simulation.git
   cd Vacuum-Weak-BB84-Simulation
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Simulations
1. Run the BB84 simulation with default parameters:
   ```bash
   python simulator.py
   ```
   This will:
   - Execute 5 simulation runs with 100 pulses each
   - Use predefined parameters for signal (μ=0.65), decoy (ν=0.08), and vacuum states
   - Save results to the `results/` directory
   - Display the filename for visualization

2. The simulation supports different attack scenarios by modifying the `attack_type` parameter in `simulator.py`:
   - `"No-Eve"`: No eavesdropper present
   - `"PNS"`: Photon Number Splitting attack
   - `"BS"`: Beam Splitter attack

### Generating Visualizations
1. List all available simulation results:
   ```bash
   python visualization.py --list
   ```

2. Generate yield plots from simulation data:
   ```bash
   python visualization.py --file FILENAME.json
   ```

3. Generate plots for specific n-photon values:
   ```bash
   python visualization.py --file FILENAME.json --n 1 3 5
   ```

4. Save plot to a specific output file:
   ```bash
   python visualization.py --file FILENAME.json --output my_plot.png
   ```

### Simulation Parameters
The simulation uses the following default parameters (configurable in `simulator.py`):

- **Protocol Parameters**:
  - Signal state mean photon number (μ): 0.65
  - Decoy state mean photon number (ν): 0.08
  - Vacuum state probability (α): 0.2
  - State percentages: Signal (75%), Decoy (12.5%), Vacuum (12.5%)

- **Channel Parameters**:
  - Channel length: 20 km
  - Channel loss: 5.6 dB
  - Receiver loss: 3.5 dB

- **Detector Parameters**:
  - Detector efficiency: 10%
  - Detector error rate: 1.4%
  - Dark count rate: 1×10⁻⁵

- **Simulation Settings**:
  - Number of runs: 5
  - Pulses per run: 100
  - N-photon yield analysis: n = 1, 2, 3, 4, 5

### Output Files
- **Simulation Results**: JSON files saved in the `results/` directory containing:
  - Expected yields for n-photon states
  - Signal and decoy state yields
  - Protocol parameters and transmission characteristics
  - Gain values for different state types

- **Visualizations**: LaTeX-formatted plots showing:
  - N-photon yield comparisons between expected, signal, and decoy states
  - Statistical analysis across multiple simulation runs
  - Publication-ready figures with proper mathematical notation

## Project Structure
```
Vacuum-Weak-BB84-Simulation/
├── simulator.py             # Main simulation script with yield analysis
├── visualization.py         # Data visualization and plotting tools
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License
│
├── protocol/               # BB84 protocol implementation
│   ├── __init__.py
│   ├── protocol.py         # Main BB84 protocol logic
│   ├── config.py           # Protocol configuration
│   ├── state.py            # Quantum state implementations
│   └── roles/              # Protocol participants
│       ├── __init__.py
│       ├── role.py         # Base role class
│       ├── sender.py       # Alice (sender) implementation
│       ├── receiver.py     # Bob (receiver) implementation
│       └── eavesdropper.py # Eve (eavesdropper) implementation
│
└── results/                # Directory for saved simulation results (created automatically)
```

## Technologies
- **Python 3.8+**: Programming language for the implementation
- **Qiskit**: Quantum computing framework for simulating quantum circuits and states
- **Qiskit Aer**: High-performance quantum circuit simulator
- **Matplotlib**: Plotting library with LaTeX support for publication-quality figures
- **NumPy**: Numerical computing library for mathematical operations
- **tqdm**: Progress bar library for simulation monitoring

## License
This project is licensed under the MIT License. See the LICENSE file for details.
