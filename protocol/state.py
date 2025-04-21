# -----------------------------------------------------------------------------
# File Name: state.py
# Author: jorgeasmz
# Date: 21/11/2024
# Description: A class representing a quantum state for an experimental BB84 protocol implementation.
# -----------------------------------------------------------------------------

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from .config import Config

import numpy as np
import random

class State:
    """
    A class representing a quantum state for an experimental BB84 protocol implementation.
    """
    def __init__(self, bit_value: int, basis: int, state_type: str):
        """
        Initialize a quantum state for BB84 protocol.
        
        Args:
            bit_value (int): The classical bit value (0 or 1)
            basis (int): The basis choice (0 for rectilinear, 1 for diagonal)
            mean_photon_number (float): Mean photon number for the state
        """
        if bit_value not in [0, 1]:
            raise ValueError("Bit value must be 0 or 1")
        if basis not in [0, 1]:
            raise ValueError("Basis must be 0 (rectilinear) or 1 (diagonal)")
        if state_type not in ['signal', 'decoy', 'vacuum']:
            raise ValueError("State type must be 'signal', 'decoy', or 'vacuum'")
            
        self.bit_value = bit_value
        self.basis = basis

        self.mean_photon_number = Config.state_type_to_mean_photon_number(state_type)

        # Determine the number of qubits based on Poisson distribution
        self.num_qubits = np.random.poisson(self.mean_photon_number)
        
        # Create quantum circuit for the state
        self.qr = QuantumRegister(self.num_qubits, 'q')
        self.cr = ClassicalRegister(self.num_qubits, 'c')
        self.circuit = QuantumCircuit(self.qr, self.cr)
        
        # Prepare the state based on bit value and basis
        self.prepare_state()
    
    def __str__(self) -> str:
        """String representation of the state."""
        base_str = "Rectilinear" if self.basis == 0 else "Diagonal"

        return (f"Bit: {self.bit_value}, Basis: {base_str}, Number of qubits: {self.num_qubits}")

    def prepare_state(self):
        """Prepare the quantum state based on bit value and basis choice."""
        if self.num_qubits == 0:
            # No need to prepare the state if there are no qubits
            return
        
        # Start from |0⟩ state
        if self.bit_value == 1:
            # Apply X gate for |1⟩ state if bit value is 1
            for qubit in range(self.num_qubits):
                self.circuit.x(self.qr[qubit])
            
        if self.basis == 1:
            # Apply Hadamard gate for diagonal basis
            for qubit in range(self.num_qubits):
                self.circuit.h(self.qr[qubit])

    def measure_state(self, measurement_basis: int):
        """
        Measure the quantum state in the given basis, combining Qiskit quantum simulation
        with realistic detector behavior.
        
        Args:
            measurement_basis (int): Basis to measure in (0 for rectilinear, 1 for diagonal)
                
        Returns:
            int or str: Measured bit value (0/1), 'No detection' or 'Wrong basis'
        """
        config = Config.get_instance()
        
        # Detector parameters
        dark_count_prob = getattr(config, 'dark_count_rate')
        efficiency = getattr(config, 'detector_efficiency')
        error_prob = getattr(config, 'detector_error_rate')
        
        # Check if bases match
        if measurement_basis != self.basis:
            return "Wrong basis"
        
        # No photons case
        if self.num_qubits == 0:
            # Consider only dark count possibility
            if np.random.random() < dark_count_prob:
                return np.random.choice([0, 1])  # 50% chance for each value
            else:
                return "No detection"
        
        # Simulate detector efficiency for each photon
        detected_photons = 0
        error_detected_photons = 0
        
        for _ in range(self.num_qubits):
            # Determine if photon is detected based on efficiency
            if np.random.random() < efficiency:
                # Determine if there's a detection error
                if np.random.random() < error_prob:
                    error_detected_photons += 1
                else:
                    detected_photons += 1
        
        # Handle detection outcomes
        if error_detected_photons > 0:
            # At least one photon incorrectly detected - bit flip
            return (self.bit_value + 1) % 2
        
        elif detected_photons == 0:
            # No photons detected - consider dark count
            if np.random.random() < dark_count_prob:
                return np.random.choice([0, 1])
            else:
                return "No detection"
        
        else:
            # At least one photon detected correctly
            # Perform actual quantum measurement with Qiskit
            
            # Create a new circuit for measurement
            meas_circuit = self.circuit.copy()
            
            # Apply basis transformation if needed
            if measurement_basis == 1:
                for qubit in range(self.num_qubits):
                    meas_circuit.h(self.qr[qubit])
                    
            # Add measurement
            meas_circuit.measure(self.qr, self.cr)
            
            # Simulate the measurement
            from qiskit import transpile
            from qiskit_aer import Aer

            backend = Aer.get_backend('qasm_simulator')
            transpiled_circuits = transpile(meas_circuit, backend)
            job = backend.run(transpiled_circuits, shots=1)
            result = job.result()
            counts = result.get_counts(meas_circuit)
            
            # Get the measured bit value
            measured_bitstring = list(counts.keys())[0]
            bit_values = [int(bit) for bit in measured_bitstring]
            majority_bit_value = max(set(bit_values), key=bit_values.count)
            
            # Consider dark count possibly altering the result
            if np.random.random() < (dark_count_prob * 0.5):
                return (majority_bit_value + 1) % 2  # Dark count error
            else:
                return majority_bit_value

    def add_noise(self, error_rate: float) -> None:
        """
        Add noise to the quantum state.
        
        Args:
            error_rate (float): Probability of applying a bit flip error
        """
        if random.random() < error_rate:
            self.circuit.x(self.qr)  # Apply bit flip error