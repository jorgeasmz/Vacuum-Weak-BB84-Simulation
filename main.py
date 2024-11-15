from protocol import Protocol

# Initialize the protocol

protocol = Protocol(num_bits=100, use_decoy_states=True, eavesdropper=False)

protocol.run_protocol()

# print("Alice's states:", [str(state) for state in protocol.alice.states])
# print("Alice's bases:", protocol.alice.bases)
# print("Alice's key:", protocol.alice.original_key)
# print("Alice's intensity types:", protocol.alice.intensity_types)
# print("Bob's bases:", protocol.bob.bases)
# print("Bob's key:", protocol.bob.measurement_results)


# print("Eve's key:", protocol.eve.measurement_results)
# print("Eve's bases:", protocol.eve.bases)
