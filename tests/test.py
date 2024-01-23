def compute_gains(init_states_df, updated_states_df):
    economic_states_df = init_states_df

    # ... (Other code remains unchanged)

    ruined = False  # signals if we have become financially "ruined"

    for month in range(months):
        # ... (Previous code remains unchanged)

        # Check for potential updates in the states
        if updated_states_df.loc[month - 1, 'variables_state'] == "updated":
            filtered_df = updated_states_df.loc[month - 1:month - 1, :]
            # Only some columns are completed
            filtered_df = filtered_df.fillna(economic_states_df.iloc[-1, :])
            inflows, strategy, misc, outflows, variables = update_parameters_from_dataframe(filtered_df, parameters)

        else:
            # Use the last state
            filtered_df = economic_states_df.iloc[-1, :]
            inflows, strategy, misc, outflows, variables = update_parameters_from_dataframe(economic_states_df, parameters)

        # ... (Rest of the loop remains unchanged)

        # Check if asset base has a positive value; if not, set the "ruined" flag to True and end the simulation
        if assets < 0:
            ruined = True
            break

        # Check if savings have a positive value; if not, set the "ruined" flag to True and end the simulation
        if sum(savings_plan_storage) < 0:
            ruined = True
            break

        # ... (Continue with the remaining code)

    # ... (Remaining code remains unchanged)

    return [inflows, income_gains_storage, income_losses_storage, income_after_saving_storage, investment_gains_storage,
            assets_ending_list, assets_starting_list, outflows, livret_A_list, livret_LDDS_list, livret_LEP_list,
            total_ending_list, ruined, variables, simulation_starting_date]
