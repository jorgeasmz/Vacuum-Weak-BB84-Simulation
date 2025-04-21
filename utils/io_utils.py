import json
import os
from datetime import datetime
from utils.utils import print_saved_results
from utils.visualization import plot_yields_boxplot

def save_simulation_results(expected_yields, signal_yields, decoy_yields, protocol_params=None):
    """
    Saves the simulation results to a JSON file.
    
    Args:
        expected_yields (dict): Expected yields.
        signal_yields (dict): Signal state yields.
        decoy_yields (dict): Decoy state yields.
        protocol_params (dict, optional): Protocol parameters used.
    
    Returns:
        str: Path to the saved file.
    """
    # Create results directory if it doesn't exist
    results_dir = 'simulation_results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{results_dir}/bb84_sim_{timestamp}.json"
    
    # Data to save
    data = {
        'expected_yields': expected_yields,
        'signal_yields': signal_yields,
        'decoy_yields': decoy_yields,
        'protocol_params': protocol_params,
        'timestamp': timestamp
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filename

def load_simulation_results(filepath):
    """
    Loads simulation results from a JSON file.
    
    Args:
        filepath (str): Path to the results file.
    
    Returns:
        tuple: (expected_yields, signal_yields, decoy_yields, protocol_params)
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return (data['expected_yields'], 
            data['signal_yields'], 
            data['decoy_yields'], 
            data.get('protocol_params'))

def list_saved_simulations(directory='simulation_results', verbose=False):
    """
    Lists all saved simulation JSON files.
    
    Args:
        directory (str): Directory where simulations are saved.
        verbose (bool): Whether to print detailed information.
    
    Returns:
        list: List of paths to simulation files.
    """
    if not os.path.exists(directory):
        return []
    
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
            if f.endswith('.json')]
    
    if verbose:
        for i, file in enumerate(files):
            print(f"{i+1}. {os.path.basename(file)}")
            
            # Show basic file information
            with open(file, 'r') as f:
                data = json.load(f)
                params = data.get('protocol_params', {})
                timestamp = data.get('timestamp', 'Unknown')
                
                is_single_run = all(len(data['expected_yields'][key]) == 1 for key in data['expected_yields'])
                type_sim = "Single run" if is_single_run else f"Multiple runs ({params.get('num_simulations', 'N/A')})"
                
                print(f"   Date: {timestamp}")
                print(f"   Type: {type_sim}")
                print(f"   Parameters: mu={params.get('mu', 'N/A')}, nu={params.get('nu', 'N/A')}")
                print()
    
    return files

def plot_from_saved_file(filepath):
    """
    Loads a saved simulation file and displays the results.
    
    Args:
        filepath (str): Path to the JSON file with results.
    """
    expected_yields, signal_yields, decoy_yields, params = load_simulation_results(filepath)
    
    # Determine if this is a single run or multiple simulations
    is_single_run = all(len(expected_yields[key]) == 1 for key in expected_yields)
    
    if is_single_run:
        print("Single run data loaded.")
        print(f"Protocol parameters: {params}")
        
        # Print results
        print_saved_results(expected_yields, signal_yields, decoy_yields, params)
    else:
        print("Multiple simulation data loaded.")
        print(f"Protocol parameters: {params}")
        
        # For multiple simulations, ask if user wants to see numerical results or graph
        display_option = input("Display (1) numerical results or (2) graph? (1/2): ")
        
        if display_option == "1":
            print_saved_results(expected_yields, signal_yields, decoy_yields, params)
        else:
            plot_yields_boxplot(signal_yields, decoy_yields, expected_yields)