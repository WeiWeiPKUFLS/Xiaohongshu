import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/weiwei/Documents/Jiban/Jiban notes list output 16Mar23.csv')

df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M')
df['month_year'] = df['time'].dt.strftime('%b-%Y')

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['month_year'].unique(), df.groupby(['month_year']).size())

ax.set_xlim(left=-0.7, right=len(df['month_year'].unique())-0.3)

ax.set_xlabel('Month and Year')
ax.set_ylabel('Number of Notes')
ax.set_xticklabels(df['month_year'].unique(), rotation=45)

# add text labels above each bar
for i in ax.containers:
    ax.bar_label(i, label_type='edge', fontsize=10)

plt.show()
