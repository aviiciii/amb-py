# import pandas lib as pd
import pandas as pd

# read by default 1st sheet of an excel file
df = pd.read_excel('file.xls')



# remove first 21 rows
df = df.iloc[19:]
# set head row
df.columns = df.iloc[0]
# remove head row
df = df[2:]

# print(df.columns)
print(df.head())



