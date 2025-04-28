# -----------------------------------------------------------------------------
# File Name: eavesdropper.py
# Author: jorgeasmz
# Last Modified: 27/04/2025
# Description: A class representing the eavesdropper in the BB84 protocol.
# -----------------------------------------------------------------------------

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from .role import Role
from protocol.state import State

import numpy as np

class Eavesdropper(Role):
    """
    A Class representing the eavesdropper in the BB84 protocol
    """

    def __init__(self):
        super().__init__('Eavesdropper')
        self.bases = None
        self.key = None
        self.forwarded_states = None
        self.extracted_qubits = None

    def __str__(self):
        return (f"Eavesdropper:\n"
                f"Bases: {self.bases}\n"
                f"Key: {self.key}\n"
                f"Extracted qubits: {len(self.extracted_qubits) if self.extracted_qubits is not None else 0}\n")

    def perform_action(self, states):
        """
        Eavesdropper performs photon number splitting attack.

        Args:
            states (np.ndarray): Array of quantum states to be intercepted.

        Returns:
            np.ndarray: Array of quantum states after interception.
        """
        num_states = len(states)
        self.forwarded_states = np.empty(num_states, dtype=object)
        self.extracted_qubits = np.empty(num_states, dtype=object)
        self.key = np.empty(num_states, dtype=object)
        
        for i, state in enumerate(states):

            if state.num_qubits == 0:
                # Eve forwards the state to Bob without interference
                self.extracted_qubits[i] = None
                self.key[i] = 'Empty'
                self.forwarded_states[i] = state

            elif state.num_qubits == 1:
                # Eve blocks the single photon and sends a vacuum state to Bob
                self.extracted_qubits[i] = None
                self.key[i] = 'Blocked'
                self.forwarded_states[i] = State(bit_value=np.random.randint(0, 2), 
                                                 basis=np.random.randint(0, 2), 
                                                 state_type='vacuum')

            elif state.num_qubits > 1:
                # Eve extracts one photon and sends n - 1 photons to Bob
                qr = QuantumRegister(1, 'q')
                cr = ClassicalRegister(1, 'c')
                circuit = QuantumCircuit(qr, cr)

                if state.bit_value == 1:
                    circuit.x(qr[0])

                if state.basis == 1:
                    circuit.h(qr[0])

                self.extracted_qubits[i] = {
                    'qr': qr,
                    'cr': cr,
                    'circuit': circuit
                }
                self.key[i] = None

                # Modify the state to have one less qubit
                state.num_qubits -= 1
                state.qr = QuantumRegister(state.num_qubits, 'q')
                state.cr = ClassicalRegister(state.num_qubits, 'c')
                state.circuit = QuantumCircuit(state.qr, state.cr)
                state.prepare_state()
                
                self.forwarded_states[i] = state

        return self.forwarded_states

    def post_process(self, sender_bases):
        """
        Post-process the intercepted states based on sender's bases.

        Args:
            sender_bases (np.ndarray): Bases used by the sender to encode the states.
        """

        if self.bases is None:
            self.bases = np.empty(len(sender_bases), dtype=int)
        
        for i, result in enumerate(self.key):
            eve_basis = sender_bases[i]
            self.bases[i] = eve_basis

            if result is None:
                # Eavesdropper measures the extracted photon in the basis the sender used
                extracted_qubit = self.extracted_qubits[i]

                if extracted_qubit is not None:
                    qr = extracted_qubit['qr']
                    cr = extracted_qubit['cr']
                    circuit = extracted_qubit['circuit']

                    # Create a new circuit to measure the extracted qubit
                    meas_circuit = QuantumCircuit(qr, cr)
                    meas_circuit.compose(circuit, inplace=True)

                    if eve_basis == 1:
                        meas_circuit.h(qr[0])
                        
                    # Add measurement
                    meas_circuit.measure(qr, cr)

                    # Simulate the measurement
                    from qiskit import transpile
                    from qiskit_aer import Aer

                    backend = Aer.get_backend('qasm_simulator')
                    transpiled_circuit = transpile(meas_circuit, backend)
                    job = backend.run(transpiled_circuit, shots=1)
                    result = job.result()
                    counts = result.get_counts(meas_circuit)

                    measured_bit = int(list(counts.keys())[0])

                    self.key[i] = measured_bit