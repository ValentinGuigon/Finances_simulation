import subprocess
import sys
import pandas as pd
from database.generate_init_states import generate_init_csv

def run_states(market_parameters, update=False):
    init_states_path = './database/generate_init_states.py'
    updated_states_path = './database/generate_new_states.py'

    # Check if the update argument is provided when running the script
    if len(sys.argv) > 1 and sys.argv[1] == '--update':
        # Run the function for init_states with update=False
        generate_init_csv(market_parameters)
        # Run other update script if needed

        # Use subprocess to run the script for updated_states with update=True
        subprocess.run(['python', updated_states_path, '--update'])
    else:
        # Run the function for init_states with update=False using default path
        generate_init_csv(market_parameters)
