import pandas as pd

df = pd.read_excel("Monitors New Project_1.xlsx", sheet_name="table")

print(len(df))

df_ = df.drop_duplicates(subset="Model", keep='last').copy()
df_.to_excel("Monitors_Jul-20.xlsx")