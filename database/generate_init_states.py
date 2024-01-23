import os
import pandas as pd
from database.get_parameters import get_starting_parameters

def create_init_states_df(market_parameters):
    personal_parameters = get_starting_parameters(market_parameters)
    data = {}
    for param_type, dictionary in personal_parameters.items():
        for key, value in dictionary.items():
            data[f"{param_type}_{key}"] = [value]

    return pd.DataFrame(data)

def generate_init_csv(market_parameters):
    df = create_init_states_df(market_parameters)

    # Save the combined dataframe to a CSV file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    starting_parameters_rel_path = os.path.join('..', 'database', 'init_states.csv')
    starting_parameters_path = os.path.abspath(os.path.join(current_dir, starting_parameters_rel_path))
    df.to_csv(starting_parameters_path, index=False)

if __name__ == "__main__":
    generate_init_csv()