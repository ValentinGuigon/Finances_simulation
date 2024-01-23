import os
import subprocess
import sys
import pandas as pd
from database.generate_init_states import generate_init_csv
from database.generate_new_states import generate_new_csv

def create_states(market_parameters, update=False):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    init_states_rel_path = os.path.join('..', 'database', 'generate_init_states.py')
    updated_states_rel_path = os.path.join('..', 'database', 'generate_new_states.py')
    
    init_states_path = os.path.abspath(os.path.join(current_dir, init_states_rel_path))
    updated_states_path = os.path.abspath(os.path.join(current_dir, updated_states_rel_path))

    # Check if the update argument is provided when running the script
    if update:
        generate_init_csv(market_parameters)
        generate_new_csv()
    else:
        generate_init_csv(market_parameters)

if __name__ == "__main__":
    create_states()
    pass
