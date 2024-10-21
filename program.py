# import pandas lib as pd
from utils import print_closing_balance, get_closing_balances, print_amb_status

amb_limit = 5000
file_name = "file.xls"


total, statement_month, statement_date_from, statement_date_to, days, closing_balances = get_closing_balances(file_name)




print_amb_status(total, statement_month, statement_date_from, statement_date_to, amb_limit, days, closing_balances)
print_closing_balance(statement_date_to, closing_balances)