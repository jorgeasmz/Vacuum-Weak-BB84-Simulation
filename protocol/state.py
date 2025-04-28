# -----------------------------------------------------------------------------
# File Name: state.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class representing a quantum state for an experimental BB84 protocol implementation.
# -----------------------------------------------------------------------------

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from .config import Config

import numpy as np

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
        if self.num_qubits > 0:
            self.qr = QuantumRegister(self.num_qubits, 'q')
            self.cr = ClassicalRegister(self.num_qubits, 'c')
            self.circuit = QuantumCircuit(self.qr, self.cr)
        
        # Prepare the state based on bit value and basis
        self.prepare_state()
    
    def __str__(self) -> str:
        """String representation of the state."""
        basis_str = "Rectilinear" if self.basis == 0 else "Diagonal"

        return (f"State:\n"
                f"Bit Value: {self.bit_value}\n"
                f"Basis: {basis_str}\n"
                f"Mean Photon Number: {self.mean_photon_number}\n"
                f"Number of Qubits: {self.num_qubits}\n")

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
        Measure the quantum state in the given basis.
        
        Args:
            measurement_basis (int): Basis to measure in (0 for rectilinear, 1 for diagonal)
                
        Returns:
            int or str: Measured bit value (0/1), 'No detection' or 'Wrong basis'
        """
        config = Config.get_instance()
        
        # Detector parameters
        transmittance = getattr(config, 'transmittance')
        detector_error_rate = getattr(config, 'detector_error_rate')
        dark_count_rate = getattr(config, 'dark_count_rate')
        
        # Check if bases match
        if measurement_basis != self.basis:
            return "Wrong basis"
        
        # No qubits detected, it can only be a dark count or no detection
        if self.num_qubits == 0:
            if np.random.random() < dark_count_rate:
                return np.random.choice([0, 1])
            else:
                return "No detection"
        
        # Simulate the detection process
        detected_qubits = 0
        error_detected_qubits = 0
        
        for _ in range(self.num_qubits):
            # Determine if a qubit is detected
            if np.random.random() < transmittance:
                # Determine if there's a detection error
                if np.random.random() < detector_error_rate:
                    error_detected_qubits += 1
                else:
                    detected_qubits += 1
        
        # Handle detection outcomes

        if error_detected_qubits > 0:
            # At least one photon incorrectly detected
            return (self.bit_value + 1) % 2
        
        elif detected_qubits == 0:
            # No qubits detected, it can only be a dark count or no detection
            if np.random.random() < dark_count_rate:
                return np.random.choice([0, 1])
            else:
                return "No detection"
        
        else:
            # At least one qubit detected correctly, measure with Qiskit
            
            # Apply basis transformation if needed
            if measurement_basis == 1:
                for qubit in range(self.num_qubits):
                    self.circuit.h(self.qr[qubit])
                    
            # Add measurement
            self.circuit.measure(self.qr, self.cr)
            
            # Simulate the measurement
            from qiskit import transpile
            from qiskit_aer import Aer

            backend = Aer.get_backend('qasm_simulator')
            transpiled_circuit = transpile(self.circuit, backend)
            job = backend.run(transpiled_circuit, shots=1)
            result = job.result()
            counts = result.get_counts(self.circuit)
            
            # Get the measured bit value
            measured_bitstring = list(counts.keys())[0]
            bit_values = [int(bit) for bit in measured_bitstring]
            majority_bit_value = max(set(bit_values), key=bit_values.count)
            
            # Consider dark count possibly altering the result
            if np.random.random() < (dark_count_rate * 0.5):
                return (majority_bit_value + 1) % 2
            else:
                return majority_bit_value