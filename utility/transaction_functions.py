# Define functions to add income and expenses
def add_income(transactions_df, date, amount):
    transactions_df.loc[len(transactions_df)] = [date, 'Income', amount]

def add_expense(transactions_df, date, amount, category):
    transactions_df.loc[len(transactions_df)] = [date, category, -amount]
