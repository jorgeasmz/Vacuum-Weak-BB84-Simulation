# Experimental BB84 Quantum Key Distribution Protocol With Decoy States

## Overview
This project implements an experimental implementation of the BB84 Quantum Key Distribution (QKD) protocol with decoy states. The BB84 protocol is a quantum cryptographic protocol that allows two parties to securely share a secret key. This implementation includes the roles of Sender, Receiver, and Eavesdropper, and simulates the protocol using Qiskit.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Instalattion](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Technologies](#technologies)
7. [License](#license)

## Features
- **Quantum State Preparation**: Simulates the preparation of quantum states for the BB84 protocol.
- **Decoy States**: Implements decoy states to enhance security against photon number splitting attacks.
- **Eavesdropper Simulation**: Simulates an eavesdropper's actions and their impact on the protocol.
- **Multiple Simulations**: Run and analyze multiple protocol executions for statistical analysis.
- **Data Persistence**: Save and load simulation results for later analysis.
- **Visualization Tools**: Graph generation for yields analysis.
- **Parameter Customization**: Configure all protocol parameters through an interactive interface.

## Installation
### Prerequisites
List any software or tools required to run the project:
- Python 3.8+
- Qiskit
- Qiskit Aer
- Matplotlib

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/project_name.git
   cd project_name
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
1. Run the main script to start the simulation tool:
   ```bash
   python main.py
2. The interactive menu allows you to:
   - Run a single protocol execution
   - Run multiple simulations for statistical analysis
   - Load and analyze saved simulation results
   - List all saved simulations

## Project Structure
      Experimental_BB84_Simulation/
      ├── main.py                  # Main entry point with interactive menu
      │
      ├── protocol/                # Protocol implementation
      │   ├── __init__.py
      │   ├── protocol.py          # BB84 protocol implementation
      │   ├── config.py            # Protocol configuration
      │   ├── state.py             # Quantum state implementations
      │   └── roles/               # Protocol participants
      │       ├── __init__.py
      │       ├── role.py          # Base role class
      │       ├── sender.py        # Alice (sender) implementation
      │       ├── receiver.py      # Bob (receiver) implementation
      │       └── eavesdropper.py  # Eve (eavesdropper) implementation
      │
      ├── simulation/              # Simulation components
      │   ├── __init__.py
      │   └── simulation.py        # Simulation execution logic
      │
      ├── utils/                   # Utility functions and helpers
      │   ├── __init__.py
      │   ├── visualization.py     # Data visualization tools
      │   ├── io_utils.py          # Data persistence
      │   └── utils.py             # Helper functions
      │
      └── simulation_results/      # Directory for saved simulation results

## Technologies
- **Python:** Programming language used for the implementation.
- **Qiskit:** Quantum computing framework used for simulating quantum circuits.
- **Matplotlib:** Library used for plotting results.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
