# Experimental BB84 Quantum Key Distribution Protocol With Decoy States

## Overview
This project implements an experimental implementation of the BB84 Quantum Key Distribution (QKD) protocol with decoy states. The BB84 protocol is a quantum cryptographic protocol that allows two parties to securely share a secret key. This implementation includes the roles of Sender, Receiver, and Eavesdropper, and simulates the protocol using Qiskit.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Technologies](#technologies)
6. [Contributing](#contributing)
7. [License](#license)

## Features
- **Quantum State Preparation**: Simulates the preparation of quantum states for the BB84 protocol.
- **Decoy States**: Implements decoy states to enhance security against photon number splitting attacks.
- **Eavesdropper Simulation**: Simulates an eavesdropper's actions and their impact on the protocol.

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
1. Run the main script to simulate the BB84 protocol:
   ```bash
   python main.py
2. Modify the parameters in main.py to customize the simulation.

## Project Structure
project_name/
│
├── roles/
│   ├── eavesdropper.py
│   ├── receiver.py
│   ├── role.py
│   └── sender.py
│
├── config.py
├── main.py
├── protocol.py
├── state.py

## Technologies
- **Python:** Programming language used for the implementation.
- **Qiskit:** Quantum computing framework used for simulating quantum circuits.
- **Matplotlib:** Library used for plotting results.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
