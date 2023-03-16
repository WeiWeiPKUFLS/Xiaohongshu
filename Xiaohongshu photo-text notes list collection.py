import os
import json
import pandas as pd
import re
from datetime import datetime

#改博主文件夹地址
directory = '/Users/weiwei/Documents/Miaoyan/Photo-text notes 16Mar23'

# create an empty dataframe to store the results
df = pd.DataFrame(columns=['note_type', 'title', 'liked_count', 'collected_count', 'comments_count', 'thumb', 'webpage_url', 'time', 'last_update_time', 'num_images'])

# iterate over each file in the directory
for filename in os.listdir(directory):
    if re.match(r"feed", filename):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            # load the json data
            data = json.load(file)

            # extract the relevant information
            for note in data['data'][0]['note_list']:
                note_type = note['type']
                title = note['title']
                liked_count = note['liked_count']
                collected_count = note['collected_count']
                comments_count = note['comments_count']
                thumb = note['qq_mini_program_info']['thumb']
                webpage_url = note['qq_mini_program_info']['webpage_url']
                time_str = note['time']
                last_update_time = note['last_update_time']
                if last_update_time != 0:
                    last_update_time = datetime.fromtimestamp(last_update_time).strftime('%d/%m/%Y %H:%M:%S')
                time = datetime.fromtimestamp(int(time_str)).strftime('%d/%m/%Y %H:%M:%S')
                num_images = len(note['images_list'])
                print(note_type, title, liked_count, collected_count, comments_count, thumb, webpage_url, time, last_update_time)

            new_row = {
                    'note_type': note_type,
                    'title': title,
                    'liked_count': liked_count,
                    'collected_count': collected_count,
                    'comments_count': comments_count,
                    'thumb': thumb,
                    'webpage_url': webpage_url,
                    'time': time,
                    'last_update_time': last_update_time,
                    'num_images': num_images
                }
            df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

# write the dataframe to a CSV file记得改博主文件夹地址
df.to_csv('/Users/weiwei/Documents/Miaoyan/Photo-text notes 16Mar23/Photo-text notes output 16Mar23.csv', encoding='utf-8-sig', index=False)




