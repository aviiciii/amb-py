# import pandas lib as pd
import pandas as pd
import re
import datetime

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
print(statement_date_from, statement_date_to, statement_month)
# print(information)





# remove first 21 rows
df = df.iloc[19:]
# set head row
df.columns = df.iloc[0]
# remove head row
df = df[2:]

# print(df.columns)
print(df.head())



# get no. of the days in the month of mm-yyyy
days = days_in_month(statement_month)
print(days)



