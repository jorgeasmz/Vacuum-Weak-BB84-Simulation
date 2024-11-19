

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from .role import Role
from state import State

import random

class Eavesdropper(Role):
    """
    A Class representing the eavesdropper in the BB84 protocol
    """

    def __init__(self):
        super().__init__('Eavesdropper')
        self.bases = []
        self.measurement_results = []
        self.forwarded_states = []
        self.extracted_qubits = []

    def __str__(self):
        return (f"Eavesdropper:\n"
                f"Bases: {self.bases}\n"
                f"Measurement results: {self.measurement_results}\n"
                f"Extracted qubits: {self.extracted_qubits}\n")

    def perform_action(self, states):
        """
        Eavesdropper performs photon number splitting attack.

        Args:
            states (list): List of quantum states to be intercepted.

        Returns:
            list[State]: List of quantum states after interception.
        """
        for state in states:

            if state.num_qubits == 0:
                # Eve forwards the state to Bob without interference
                self.extracted_qubits.append(None)
                self.measurement_results.append('Empty')

            elif state.num_qubits == 1:
                # Eve blocks the single photon and sends a vacuum state to Bob
                self.extracted_qubits.append(None)
                self.measurement_results.append('Blocked')
                state = State(bit_value=random.choice([0, 1]), 
                              basis=random.choice([0, 1]), 
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

                self.extracted_qubits.append({
                    'qr': qr,
                    'cr': cr,
                    'circuit': circuit
                })
                self.measurement_results.append(None)

                state.num_qubits -= 1
                state.qr = QuantumRegister(state.num_qubits, 'q')
                state.cr = ClassicalRegister(state.num_qubits, 'c')
                state.circuit = QuantumCircuit(state.qr, state.cr)
                state.prepare_state()

            self.forwarded_states.append(state)

        return self.forwarded_states

    def post_process(self, sender_bases):
        """
        Post-process the intercepted states based on sender's bases.

        Args:
            sender_bases (list): Bases used by the sender to encode the states.
        """
        for i, result in enumerate(self.measurement_results):

            eve_basis = sender_bases[i]
            self.bases.append(eve_basis)

            if result is None:
                # Eve measures the extracted photon in the basis Alice used
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

                    # Simulate the measurement
                    from qiskit import transpile
                    from qiskit_aer import Aer

                    backend = Aer.get_backend('qasm_simulator')
                    transpiled_circuits = transpile(meas_circuit, backend)
                    job = backend.run(transpiled_circuits, shots=1)
                    result = job.result()
                    counts = result.get_counts(meas_circuit)

                    measured_bit = int(list(counts.keys())[0])

                    self.measurement_results[i] = measured_bit