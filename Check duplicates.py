import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statistics

df = pd.read_csv('/Users/weiwei/Documents/Zhichuantao/Zhichuantao notes 20Mar23.csv', encoding='utf-8-sig')

duplicates = df[df.duplicated()]

if duplicates.empty:
    print("There are no duplicate rows in the CSV file.")
else:
    print("Duplicate rows exist in the CSV file.")

# Count the number of duplicate rows
num_duplicates = len(df[df.duplicated()])

if num_duplicates == 0:
    print("There are no duplicate rows in the CSV file.")
else:
    print(f"There are {num_duplicates} duplicate rows in the CSV file.")

# Remove duplicate rows
df = df.drop_duplicates()

# Write the new DataFrame to a CSV file
df.to_csv('/Users/weiwei/Documents/Zhichuantao/Zhichuantao notes 20Mar23_without_duplicates.csv', encoding='utf-8-sig', index=False)

