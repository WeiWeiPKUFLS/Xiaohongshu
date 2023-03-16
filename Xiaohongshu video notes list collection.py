import os
import json
import pandas as pd
import re
from datetime import datetime

#记得改博主文件夹
directory = '/Users/weiwei/Documents/Miaoyan/Video notes 16Mar23'

df = pd.DataFrame(columns=['note_type', 'title', 'liked_count', 'collected_count', 'comments_count', 'thumb', 'webpage_url', 'time', 'last_update_time', 'duration', 'identifier'])

for filename in os.listdir(directory):
    if re.match(r"videofeed", filename):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            for note in data['data']:
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
                duration = note['video_info_v2']['capa']['duration']
                
                # Create a unique identifier based on the values of 'title' and 'webpage_url'
                identifier = f"{title}_{webpage_url}"
                if identifier not in df['identifier'].values:
                    # Add the identifier to the new row
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
                            'identifier': identifier,
                            'duration': duration
                            }
                    df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

# Drop the 'identifier' column before saving to CSV记得改博主文件夹
df.drop(columns=['identifier'], inplace=True)
df.to_csv('/Users/weiwei/Documents/Miaoyan/Video notes 16Mar23/Video notes list output 16Mar23.csv', encoding='utf-8-sig', index=False)

