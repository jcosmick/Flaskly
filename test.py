import pandas as pd
abs_path = r'.\uploads'
df = pd.read_csv(abs_path+'/provincia-regione-sigla.csv')

print(df.columns.to_list())
print(df["Sigla"].to_list())
