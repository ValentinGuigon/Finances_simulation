def update_parameters_from_dataframe(dataframe, input_dict):
    updated_dicts = {}

    # Iterate through keys in the input dictionary
    for prefix, inner_dict in input_dict.items():
        if not isinstance(inner_dict, dict):
            raise ValueError(f"Value for key '{prefix}' must be a dictionary.")

        # Extract data from the DataFrame for the given prefix
        prefix_columns = [col for col in dataframe.columns if col.startswith(f"{prefix}_")]
        prefix_dict = {col.split(f"{prefix}_")[1]: dataframe.at[0, col] for col in prefix_columns}

        # Create a new dictionary with updated values
        updated_dict = {**inner_dict, **prefix_dict}

        updated_dicts[prefix] = updated_dict

    return tuple(updated_dicts.values())

# Assuming you have a dictionary named 'all_parameters'
all_parameters = {
    'inflows': {'active_annual_income': 72000, 'livret_A': 24040.125, 'livret_LDDS': 23695.875},
    'strategy': {'some_strategy_param': 0.05, 'another_strategy_param': 0.1},
    'misc': {'some_misc_param': 'value'},
    'outflows': {'expenses_1': 1000, 'expenses_2': 1500},
    'variables': {'start_date': '01/01/2022', 'years': 10}
}

# Call the function with the modified signature
result_tuple = update_parameters_from_dataframe(economic_states_df, all_parameters)

# The result_tuple will contain the updated dictionaries
