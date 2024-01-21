import pandas as pd
import numpy as np


import pandas as pd

def parameters_to_dataframe(parameters):
    data = {}
    for param_type, param_dict in parameters.items():
        for key, value in param_dict.items():
            column_name = f"{param_type}_{key}"
            data[column_name] = [value]
    return pd.DataFrame(data)


def update_state_df(df1, df2):
    merged_df = pd.concat([df1, df2], ignore_index=True)

    return merged_df



# def apply_shocking_state(dataframe, starting_period, ending_period, **kwargs):
#     """
#     Apply shocks to specified columns in the dataframe.

#     Parameters:
#     - dataframe: pd.DataFrame
#         The dataframe to be modified.
#     - starting_period: int
#         The starting period (row) to apply shocks.
#     - ending_period: int
#         The ending period (row) to apply shocks.
#     - **kwargs:
#         Dictionary of parameters and their corresponding new values.
#     """

#     for column, value in kwargs.items():
#         if column in dataframe.columns:
#             dataframe.loc[starting_period:ending_period, column] = value
#         else:
#             raise KeyError(f"Column {column} not found in the DataFrame.")

#     return dataframe


def unpack_parameters_from_dataframe(dataframe, *desired_prefixes):
    parameters = {}

    # Iterate through desired prefixes and create dictionaries
    for prefix in desired_prefixes:
        prefix_columns = [col for col in dataframe.columns if col.startswith(f"{prefix}_")]
        prefix_dict = {col.split(f"{prefix}_")[1]: dataframe.at[0, col] for col in prefix_columns}
        parameters[prefix] = prefix_dict

    return tuple(parameters[prefix] for prefix in desired_prefixes)


def update_parameters_from_dataframe(dataframe, input_dict):
    updated_dicts = {}

    # Iterate through keys in the input dictionary
    for prefix, inner_dict in input_dict.items():
        if not isinstance(inner_dict, dict):
            raise ValueError(f"Value for key '{prefix}' must be a dictionary.")

        # Extract data from the DataFrame for the given prefix
        prefix_columns = [col for col in dataframe.columns if col.startswith(f"{prefix}_")]

        # Check if the dataframe is not empty
        if not dataframe.empty:
            prefix_dict = {col.split(f"{prefix}_")[1]: dataframe.at[dataframe.index[-1], col] for col in prefix_columns}
        else:
            prefix_dict = {}

        # Print statements for debugging

        # Create a new dictionary with updated values
        updated_inner_dict = {inner_key: prefix_dict[inner_key] if inner_key in prefix_dict else value for inner_key, value in inner_dict.items()}
        updated_dicts[prefix] = updated_inner_dict

    # Create new dictionaries for each type
    inflows = updated_dicts.get('inflows', {})
    strategy = updated_dicts.get('strategy', {})
    misc = updated_dicts.get('misc', {})
    outflows = updated_dicts.get('outflows', {})
    variables = updated_dicts.get('variables', {})

    return inflows, strategy, misc, outflows, variables
