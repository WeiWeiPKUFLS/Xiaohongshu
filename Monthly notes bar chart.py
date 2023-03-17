import pandas as pd
import datetime
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/weiwei/Documents/Huanhuan/Huanhuan notes list output 15Mar23.csv')

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M')

# Create a new column for year and month
df['year_month'] = df['time'].dt.strftime('%Y-%m')

# Count the number of URLs for each year_month
url_count = df.groupby('year_month')['webpage_url'].count()

# Create a list of all the year_month values
year_month_list = pd.date_range(start=url_count.index.min(), end=url_count.index.max(), freq='MS').strftime('%Y-%m').tolist()

# Create a dictionary to hold the counts for each year_month
url_count_dict = dict.fromkeys(year_month_list, 0)

# Update the counts in the dictionary with the values from the url_count series
url_count_dict.update(url_count.to_dict())

# Create a bar chart
plt.bar(url_count_dict.keys(), url_count_dict.values())

# Add text labels to the bars
for i, v in enumerate(url_count_dict.values()):
    plt.text(i, v, str(v), ha='center', va='bottom')

# Add x-label and y-label
plt.xlabel('Month and Year')
plt.ylabel('Number of Notes')

# Rotate the x-axis labels
plt.xticks(rotation=45)

# Show the plot
plt.show()
