import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV file and exclude rows with time in March 2023
df = pd.read_csv('/Users/weiwei/Documents/Participant stats/Huanhuan notes list output 15Mar23.csv')
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M')
df = df[df['time'].dt.strftime('%Y-%m') != '2023-03']

# group the liked_count values into ranges and calculate counts and percentages
bins = [0, 500, 1000, 5000, 10000, float('inf')]
labels = ['0-500', '500-1000', '1000-5000', '5000-10000', '10000+']
df['range'] = pd.cut(df['liked_count'], bins=bins, labels=labels)
range_counts = df['range'].value_counts()
range_percentages = round(range_counts / range_counts.sum() * 100)

# create the pie chart with labels and percentages
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(range_counts, labels=labels, autopct='%1.0f%%', startangle=90, textprops=dict(color="w"))

# set the text properties for the labels and percentages
for text in texts:
    text.set_color('black')
    text.set_fontsize(14)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(14)

# add the actual figures to the labels
for i, wedge in enumerate(wedges):
    wedge.set_edgecolor('white')
    texts[i].set_text('{}\n{}'.format(labels[i], range_counts[labels[i]]))

# add the legend to the top-right corner
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))

# show the plot
plt.show()
