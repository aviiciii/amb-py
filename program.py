# import pandas lib as pd
import pandas as pd
import re
import datetime

amb_limit = 20000

def days_in_month(date):
    mm, yyyy = map(int, date.split('/'))
    return (datetime.date(yyyy, (mm)+1, 1) - datetime.date(yyyy, mm, 1)).days

# read by default 1st sheet of an excel file
df = pd.read_excel('file.xls')

# get the row 5 to 18
info = df.iloc[3:19]
information = []
statement_date = None

for i in range(0, len(info)):
    if type(info.iloc[i][4]) is str:
        information.append(info.iloc[i][4])

    if not statement_date:
        i = info.iloc[i][0]

        if type(i)==str and i.startswith('Statement From'):
            statement_date = i

statement_date_from, statement_date_to = re.findall(r'\d{2}/\d{2}/\d{4}', statement_date)
statement_month = re.findall(r'\d{2}/\d{4}', statement_date)[0]
statement_date_from = int(statement_date_from[:2])
statement_date_to = int(statement_date_to[:2])
# print(statement_date_from, statement_date_to, statement_month)
# print(information)





# remove first 21 rows
df = df.iloc[19:]
# set head row
df.columns = df.iloc[0]
# remove head row
df = df[2:]

# print(df.columns)
# print(df.head())

closing_balances ={}

# get the date of the statement
for i in range(len(df)):
    date = df.iloc[i]['Date']
    closing_balance = df.iloc[i]['Closing Balance']
    if (type(date) is float) or (type(date) is str and date.startswith('*')):
        break
    if date != df.iloc[i+1][0]:
        date= int(date[:2])
        closing_balances[date] = closing_balance



# get no. of the days in the month of mm-yyyy
days = days_in_month(statement_month)
# print(days)

total = 0
for i in range(1, statement_date_to):
    if i not in closing_balances:
        closing_balances[i] = closing_balances[i-1]

    total += closing_balances[i]

# print(closing_balances)

# check amb cleared
amb = total/days

if amb > amb_limit:
    print('AMC is cleared')
else:
    print('AMC is not cleared by', amb_limit-amb)


current_dayaverage = total/statement_date_to
print('Current day average:', current_dayaverage)

total_amb_limit = amb_limit * days
remaining = total_amb_limit - total
print('Remaining amount to clear AMC:', remaining)
days_remaining = days - statement_date_to
# how to add to clear
if amb < amb_limit:
    print('You need to keep', remaining/days_remaining, 'per day to clear AMC')


        





