import pandas as pd

# Load the correct CSV file
csv_file_path = 'D:/BankLLM/data/customer_profile_data.csv'  # Update the file name
customer_data = pd.read_csv(csv_file_path, encoding="utf-8", on_bad_lines="skip")

# Define the SQL statement template
sql_template = """
INSERT INTO CustomerProfile (
    CustomerID, FirstName, LastName, Gender, Email, Phone, Age, City, Country,
    CurrentBalance, Currency, TotalTransactions, TotalDeposits, TotalWithdrawals,
    AverageTransactionAmount, TotalCashback, LastTransactionDate, PreferredContactMethod,
    AverageMonthlySpending, HighestTransactionAmount, LowestTransactionAmount, 
    TotalNumberOfAccounts, AccountStatus, RiskProfile, DepositStatus, LoanStatus, 
    InternationalTransactionIndicator, VATUserStatus, TotalVATRefundAmount, DeviceModel, 
    AppVersion, RecentActivityFlag, PreferredLanguage, Delivery, PlasticCard
) VALUES
"""

# Generate SQL statements
sql_statements = []
for index, row in customer_data.iterrows():
    values = tuple(row.fillna("NULL"))  # Replace NaN with NULL values
    sql_statements.append(sql_template + str(values) + ";")

# Write to SQL file
with open('D:/BankLLM/data/customer_profile_insert_statements.sql', 'w', encoding="utf-8") as f:
    for statement in sql_statements:
        f.write(statement + "\n")

print("SQL insert statements have been written successfully!")
