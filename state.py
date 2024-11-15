from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from typing import Dict

import numpy as np
import random

class State:
    """
    A class representing a quantum state for an experimental BB84 protocol implementation.
    """
    
    def __init__(self, bit_value: int, basis: int, mean_photon_number = float):
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
            
        self.bit_value = bit_value
        self.basis = basis
        self.mean_photon_number = mean_photon_number
        
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

    def measure_state(self, measurement_basis: int) -> int:
        """
        Measure the quantum state in the given basis.
        
        Args:
            measurement_basis (int): Basis to measure in (0 for rectilinear, 1 for diagonal)
            
        Returns:
            int: Measured bit value
        """
        if self.num_qubits == 0:
            # Simulate a dark count (false detection) with a certain probability (equal to the dark count rate)
            if np.random.random() < 10e-5:
                return np.random.choice([0, 1])
            else:
                return None  # No detection

        # Create a new circuit for measurement
        meas_circuit = self.circuit.copy()
        
        # If measuring in diagonal basis, apply H gate before measurement
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
        
        # Return the measured bit value
        measured_bitstring = list(counts.keys())[0]
        
        # Return the majority bit value if there are multiple qubits
        bit_values = [int(bit) for bit in measured_bitstring]
        majority_bit_value = max(set(bit_values), key=bit_values.count)

        return majority_bit_value
    
    def get_photon_number_distribution(self) -> Dict[int, float]:
        """
        Calculate the photon number distribution based on Poisson statistics.
        
        Returns:
            Dict[int, float]: Dictionary mapping photon numbers to their probabilities
        """
        mean = self.mean_photon_number
        max_photons = 10  # Maximum number of photons to consider
        distribution = {}
        
        for n in range(max_photons):
            # Calculate Poisson probability: P(n) = μⁿe^(-μ)/n!
            prob = (mean**n * np.exp(-mean)) / np.math.factorial(n)
            distribution[n] = prob
            
        return distribution    

    def add_noise(self, error_rate: float) -> None:
        """
        Add noise to the quantum state.
        
        Args:
            error_rate (float): Probability of applying a bit flip error
        """
        if random.random() < error_rate:
            self.circuit.x(self.qr)  # Apply bit flip error