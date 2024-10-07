# import pandas lib as pd
import pandas as pd
import re
import datetime

amb_limit = 5000
file_name = "file.xls"


def days_in_month(date):
    mm, yyyy = map(int, date.split("/"))
    return (datetime.date(yyyy, (mm) + 1, 1) - datetime.date(yyyy, mm, 1)).days


def def_statement_date(df):
    # get the row 5 to 18
    info = df.iloc[3:19]
    information = []
    statement_date = None

    for i in range(0, len(info)):
        if type(info.iloc[i][4]) is str:
            information.append(info.iloc[i][4])

        if not statement_date:
            i = info.iloc[i][0]

            if type(i) == str and i.startswith("Statement From"):
                statement_date = i

    statement_date_from, statement_date_to = re.findall(
        r"\d{2}/\d{2}/\d{4}", statement_date
    )
    statement_month = re.findall(r"\d{2}/\d{4}", statement_date)[0]
    statement_date_from = int(statement_date_from[:2])
    statement_date_to = int(statement_date_to[:2])

    return statement_month, statement_date_from, statement_date_to


def print_closing_balance():
    print("\n", "--  Closing Balances  --", "\n")
    temp = 0
    for i in range(1, statement_date_to+1):
        temp += closing_balances[i]
        print(f"Day {i}: {closing_balances[i]}, AMB: {temp/i:2f}")

# read by default 1st sheet of an excel file
df = pd.read_excel(file_name)

# get stuff
statement_month, statement_date_from, statement_date_to = def_statement_date(df)
days = days_in_month(statement_month)


# remove the summary and set the columns
df = df.iloc[19:]
df.columns = df.iloc[0]
df = df[2:]

# get the opening balance
# iterate through the rows till "opening balance" is found
opening_balance = None
for i in range(len(df)):
    if type(df.iloc[i][0]) == str and df.iloc[i][0].startswith("Opening Balance"):
        opening_balance = df.iloc[i + 1][0]


closing_balances = {}

# get the closing balance of each day
for i in range(len(df)):
    date = df.iloc[i]["Date"]
    closing_balance = df.iloc[i]["Closing Balance"]
    if (type(date) is float) or (type(date) is str and date.startswith("*")):
        break
    if date != df.iloc[i + 1][0]:
        date = int(date[:2])
        closing_balances[date] = closing_balance

# get the closing balances of all days and the total
total = 0

for i in range(1, statement_date_to+1):
    if i not in closing_balances:
        if i == 1:
            closing_balances[i] = opening_balance
        else:
            closing_balances[i] = closing_balances[i - 1]

    total += closing_balances[i]
    
    
# calculate the total amount to maintain AMB
total_amb = amb_limit * days
current_amb = total / statement_date_to

# find deviance
deviance = current_amb - amb_limit

if total > total_amb:
    print("\n", "--  AMB Cleared  --", "\n")
    print(
        f"Statement Date: {statement_date_from}/{statement_month} to {statement_date_to}/{statement_month}"
    )

    print(
        "Curent AMB (till statement date):",
        "{:.2f}".format(current_amb),
        "(+" + "{:.2f}".format((deviance)) + ")",
    )
else:
    print("\n", "--  AMB Not Cleared  --", "\n")
    print(
        f"Statement Date: {statement_date_from}/{statement_month} to {statement_date_to}/{statement_month}"
    )
    # calculate stuff
    if total < total_amb:
        # find lacking amount
        lacking_amount = total_amb - total
        lacking_amount_per_day = lacking_amount / statement_date_to

        # get the amount to keep per day
        days_left = days - statement_date_to
        amount_to_keep_per_day = lacking_amount / days_left

    if deviance < 0:
        print(
            "Curent AMB (till statement date):",
            "{:.2f}".format(current_amb),
            "(" + "{:.2f}".format((deviance)) + ")",
        )
    else:
        print(
            "Curent AMB (till statement date):",
            "{:.2f}".format(current_amb),
            "(+" + "{:.2f}".format((deviance)) + ")",
        )
    print(
        "You need to keep",
        "{:.2f}".format(amount_to_keep_per_day),
        "per day to maintain AMB",
        "(" + str(days_left) + " days)",
    )
print_closing_balance()