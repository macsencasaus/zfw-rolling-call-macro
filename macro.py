import keyboard
import json
import os
import argparse
import threading

from functools import partial
from time import time

def get_arguments() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser(description='Creates macros for ZFW VRC rolling call alias command.')

    parser.add_argument('-c', '--config-file',
                        default='config.json',
                        type=str,
                        help='Name of the JSON config file, Default: config.json')
    parser.add_argument('-f', '--facility-flow',
                        default='dfw-south',
                        type=str,
                        help='Defines the facility and flow for the keybinds, Default: dfw-south')
    
    arguments = parser.parse_args()
    return arguments

def read_json_config(file_path: str, facility_flow: str) -> dict:
    """Read in config JSON file to create the macro

    Args:
        file_path (str): path of the config JSON file
        facility_flow (str): the facility and flow selected

    Returns:
        dict: contains all the keys in the JSON file
    """
    
    # Make sure config file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Specified config file does not exist: {file_path}')
    
    with(open(file_path, 'r')) as json_file:
        config = json.load(json_file)
        
    required_keys = {'alias', 'facility-flow'}
    required_facility_keys = {'departure_sector_id', 'keybind_runway_dict'}
    
    # Makes sure the required keys exist
    missing_keys = required_keys.difference(set(config.keys())) | \
        required_facility_keys.difference(set(config['facility-flow'][facility_flow].keys()))
        
    if missing_keys:
        raise KeyError(f"Missing required key(s) in JSON config file: \
                       {', '.join(list(missing_keys))}")
        
    return config

if __name__ == '__main__':
    
    # Start stopwatch
    script_start = time()
    
    # Get command line arguments
    args = get_arguments()
    facility_flow = args.facility_flow

    # Get JSON config file
    config = read_json_config(args.config_file, facility_flow)
    
    # Get config data
    alias = config['alias']
    facility_flow_dict = config['facility-flow'][facility_flow]
    departure_sector_id = facility_flow_dict['departure_sector_id']
    keybind_runway_dict = facility_flow_dict['keybind_runway_dict']
    
    def create_sector_command(departure_sector_id: str):      
        def create_command(runway: str):
            keyboard.write(f'{alias} {departure_sector_id} {runway}')
        return create_command
    
    sector_command = create_sector_command(departure_sector_id)
            
    # Add hotkeys
    def add_hotkeys():
        for keybind, runway in keybind_runway_dict.items():
            try: keyboard.remove_hotkey(keybind)
            except: pass
            keyboard.add_hotkey(keybind, partial(sector_command, runway))
        
    add_hotkeys()

    # Create thread to change departure sector id
    def input_thread():
        global sector_command
        while True:
            new_departure_sector_id = input("New departure sector id: ")
            sector_command = create_sector_command(new_departure_sector_id)
            add_hotkeys()
        
    # Create thread for user input
    input_thread = threading.Thread(target=input_thread)
    input_thread.daemon = True
    input_thread.start()
    
    try:
        print(f"Running {args.config_file}. Press 'Ctrl+C' to exit.")
        keyboard.wait()
    except KeyboardInterrupt:
        print('')
        print(f'Program interrupted. Total runtime: {time()-script_start:.1f}s')
    finally:
        keyboard.unhook_all()