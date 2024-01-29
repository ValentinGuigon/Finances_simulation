import numpy as np
import matplotlib.pyplot as plt

def calculate_amount_without_interest(principal, total_addition, addition_frequency, periods):
    amounts = []
    amount = principal

    for day in range(periods):
        if day % addition_frequency == 0 or day == 0:
            amount += total_addition / (periods / addition_frequency)
        amounts.append(amount)

    return amounts

def calculate_amount_with_interest(principal, interest_rate, total_addition, addition_frequency, compound_frequency, periods):
    amounts = []
    amount = principal

    for day in range(periods):
        if day % addition_frequency == 0 or day == 0:
            amount += total_addition / (periods / addition_frequency)

        if (day + 1) % (periods // compound_frequency) == 0 and day != periods - 1:
            compound_rate = 1 + interest_rate / compound_frequency
            amount *= compound_rate

        amounts.append(amount)

    return amounts

def plot_results(scenarios, years):
    for scenario in scenarios:
        without_interest = calculate_amount_without_interest(scenario['principal'], scenario['total_addition'], scenario['addition_frequency'], scenario['periods'])
        with_interest = calculate_amount_with_interest(scenario['principal'], scenario['interest_rate'], scenario['total_addition'], scenario['addition_frequency'], scenario['compound_frequency'], scenario['periods'])

        plt.plot(range(1, len(with_interest) + 1), with_interest, label=f"{scenario['name']} - With Interest")
        plt.plot(range(1, len(without_interest) + 1), without_interest, linestyle='dotted', label=f"{scenario['name']} - Without Interest")

    plt.title(f"Compound and Addition Scenarios over {years} Years")
    plt.xlabel("Days")
    plt.ylabel("Amount")
    plt.legend()
    plt.show()

def print_difference(scenario, years):
    without_interest = calculate_amount_without_interest(scenario['principal'], scenario['total_addition'], scenario['addition_frequency'], scenario['periods'])
    with_interest = calculate_amount_with_interest(scenario['principal'], scenario['interest_rate'], scenario['total_addition'], scenario['addition_frequency'], scenario['compound_frequency'], scenario['periods'])
    
    difference = with_interest[-1] - without_interest[-1]
    print(f"Difference for {scenario['name']} over {years} years: {difference:.2f}")

# Scenarios
amount_per_year = 6000
years_to_simulate = 3

scenario1 = {'name': 'Scenario 1', 'principal': 0, 'interest_rate': 0.06, 
'total_addition': amount_per_year*years_to_simulate, 'addition_frequency': 12, 
'compound_frequency': 6, 'periods': 365 * years_to_simulate}

scenario2 = {'name': 'Scenario 2', 'principal': 0, 'interest_rate': 0.06, 
'total_addition': amount_per_year*years_to_simulate, 'addition_frequency': 12, 
'compound_frequency': 12, 'periods': 365 * years_to_simulate}

scenario3 = {'name': 'Scenario 3', 'principal': 0, 'interest_rate': 0.06, 
'total_addition': amount_per_year*years_to_simulate, 'addition_frequency': 12, 
'compound_frequency': 24, 'periods': 365 * years_to_simulate}

# Run scenarios
scenarios = [scenario1, scenario2, scenario3]
plot_results(scenarios, years_to_simulate)

# Print differences for all scenarios
for scenario in scenarios:
    print_difference(scenario, years_to_simulate)