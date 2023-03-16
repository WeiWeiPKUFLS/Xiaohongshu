import json
import pandas as pd
from datetime import datetime
import requests
from urllib.parse import urlparse
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


#import json file 记得修改具体博主的文件夹和json文档
with open('/Users/weiwei/Documents/Rourou/Rourou hey_gallery 16Mar23.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#put the info about heys into a csv
#修改博主文件夹和csv名字

items1 = data['data'][0]['hey_list']
items2 = data['data'][1]['hey_list']
items3 = data['data'][2]['hey_list']
items = items1 + items2 + items3  # concatenate both lists
urls = [item['url'] for item in items]
times = [datetime.fromtimestamp(item['time']).strftime('%d-%m-%Y %H:%M') for item in items]
df = pd.DataFrame({'time': times, 'url': urls})
df.to_csv('/Users/weiwei/Documents/Rourou/Hey 16Mar23/Rourou hey_gallery 16Mar23.csv', index=False)

#downloading the files 修改博主文件夹和文件名
directory = '/Users/weiwei/Documents/Rourou/Hey 16Mar23'
for index, row in df.iterrows():
    url = row['url']
    response = requests.get(url, verify=True)
    timestamp = row['time']
    content_type = response.headers['content-type']
    file_extension = '.jpg' if 'image' in content_type else '.mp4'
    file_name = f"Rourou Hey {timestamp}{file_extension}"
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as f:
        f.write(response.content)
