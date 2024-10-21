# import pandas lib as pd
from utils import print_closing_balance, get_closing_balances, print_amb_status

amb_limit = 5000
try:
    file_name = "file.xls"
    total, statement_month, statement_date_from, statement_date_to, days, closing_balances = get_closing_balances(file_name)
except FileNotFoundError:
    print("File not found. Please check the file path.")
    exit()
else:
    print("File found successfully.")
    
# menu
while True:
    print("\n", "--  Menu  --", "\n")
    print("1. Print AMB Status")
    print("2. Print Closing Balances")
    print("3. Amount to maintain to clear in N days")
    print("4. Days to clear AMB with given amount")
    print("5. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid choice. Please enter a number.")
        continue
    if choice == 1:
        print_amb_status(total, statement_month, statement_date_from, statement_date_to, amb_limit, days, closing_balances)
    elif choice == 2:
        print_closing_balance(statement_date_to, closing_balances)
    else:
        exit()





