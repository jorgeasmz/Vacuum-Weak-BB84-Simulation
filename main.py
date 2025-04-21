from protocol.protocol import Protocol
from simulation.simulation import run_multiple_simulations
from utils.visualization import plot_yields_boxplot
from utils.io_utils import *
from utils.utils import *

import matplotlib.pyplot as plt

# Main configuration
nth_photon = 5
num_simulations = 100

def main():
    print("BB84 Simulation Tool")
    print("1. Run a single protocol execution")
    print("2. Run multiple simulations")
    print("3. Load saved results")
    print("4. List saved simulations")
    print("5. Exit")
    
    choice = input("Select an option: ")

    if choice == "1":
        # Run a single protocol execution
        print("Enter protocol parameters:")
        params = get_protocol_parameters()
        
        protocol = Protocol(num_bits=params['num_bits'], 
                        use_decoy_states=params['use_decoy_states'], 
                        eavesdropper=params['eavesdropper'], 
                        mu=params['mu'], 
                        nu=params['nu'], 
                        dark_count_rate=params['dark_count_rate'], 
                        channel_loss=params['channel_loss'],
                        channel_length=params['channel_length'],
                        receiver_loss=params['receiver_loss'],
                        detector_efficiency=params['detector_efficiency'],
                        detector_error_rate=params['detector_error_rate'],
                        signal_percentage=params['signal_percentage'], 
                        decoy_percentage=params['decoy_percentage'], 
                        vacuum_percentage=params['vacuum_percentage'])

        protocol.run_protocol()
        
        print("\n--- Protocol Results ---")
        print_protocol_results(protocol)
        
        expected, signal, decoy, params = convert_single_run_to_dict(protocol, nth_photon, params)
        saved_file = save_simulation_results(expected, signal, decoy, params)
        print(f"Results saved to: {saved_file}")
    
    elif choice == "2":
        # Run multiple simulations
        num = int(input(f"Number of simulations (default {num_simulations}): ") or num_simulations)
        
        print("Enter protocol parameters:")
        params = get_protocol_parameters()
        
        print(f"Running {num} simulations. This may take some time...")
        expected_yields, signal_yields, decoy_yields = run_multiple_simulations(nth_photon, num, params)
        
        # Show graph
        plot_yields_boxplot(signal_yields, decoy_yields, expected_yields)
        
        # Add number of simulations to parameters
        params['num_simulations'] = num
            
        saved_file = save_simulation_results(expected_yields, signal_yields, decoy_yields, params)
        print(f"Results saved to: {saved_file}")
    
    elif choice == "3":
        # Load saved results
        files = list_saved_simulations()
        if not files:
            print("No saved simulations found.")
            return True
        
        print("Available simulations:")
        for i, file in enumerate(files):
            print(f"{i+1}. {os.path.basename(file)}")
        
        file_idx = int(input("Select file number to load: ")) - 1
        if 0 <= file_idx < len(files):
            plot_from_saved_file(files[file_idx])
        else:
            print("Invalid selection.")
    
    elif choice == "4":
        # List saved simulations
        files = list_saved_simulations()
        if not files:
            print("No saved simulations found.")
            return True
        
        print("Available simulations:")
        list_saved_simulations(verbose=True)
    
    elif choice == "5":
        print("Exiting...")
        return False
    
    else:
        print("Invalid option.")
    
    return True

# Execute the main menu
if __name__ == "__main__":
    import os
    running = True
    while running:
        running = main()