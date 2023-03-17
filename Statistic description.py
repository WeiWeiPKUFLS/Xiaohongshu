import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statistics

df = pd.read_csv('/Users/weiwei/Documents/Participant stats/Xueer notes list output 16Mar23.csv')

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

# Remove values from the year_month of "2023-03"
url_count_dict = {k:v for k,v in url_count_dict.items() if k[:7] != "2023-03"}


# Calculate and print the mean, median, mode, and range of url_count_dict.values()
url_values = list(url_count_dict.values())
mean = statistics.mean(url_values)
median = statistics.median(url_values)
mode = statistics.mode(url_values)
range_val = max(url_values) - min(url_values)
print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)
print("Range:", range_val)
