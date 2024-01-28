import matplotlib.pyplot as plt
import numpy as np

def compound_interest_with_addition(P, r, n, t, yearly_addition):
    amount = P
    amounts = [amount]

    for year in t[1:]:
        amount = amount * (1 + r/n) + yearly_addition
        amounts.append(amount)

    return np.array(amounts)

# Parameters for three different compound interest scenarios
params1 = {'P': 10000, 'r': 0.05, 'n': 12, 't': np.linspace(0, 10, 100), 'yearly_addition': 1000}
params2 = {'P': 20000, 'r': 0.05, 'n': 12, 't': np.linspace(0, 10, 100), 'yearly_addition': 1000}
params3 = {'P': 30000, 'r': 0.05, 'n': 12, 't': np.linspace(0, 10, 100), 'yearly_addition': 1000}

# Calculate compound interest with annual addition for each scenario
A1 = compound_interest_with_addition(**params1)
A2 = compound_interest_with_addition(**params2)
A3 = compound_interest_with_addition(**params3)

# Plot the compound interest with annual addition for each scenario
plt.plot(params1['t'], A1, label='Scenario 1')
plt.plot(params2['t'], A2, label='Scenario 2')
plt.plot(params3['t'], A3, label='Scenario 3')

# Calculate and plot the distance between scenarios over time
distance_1_2 = np.abs(A1 - A2)
distance_2_3 = np.abs(A2 - A3)
distance_1_3 = np.abs(A1 - A3)

plt.plot(params1['t'], distance_1_2, linestyle='--', label='Distance between 1 and 2')
plt.plot(params2['t'], distance_2_3, linestyle='--', label='Distance between 2 and 3')
plt.plot(params3['t'], distance_1_3, linestyle='--', label='Distance between 1 and 3')

# Add labels and title
plt.xlabel('Time (years)')
plt.ylabel('Amount ($)')
plt.title('Compound Interest With Annual Addition Over Time')

# Display the legend
plt.legend()

# Show the plot
plt.show()
