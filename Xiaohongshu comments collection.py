import os
import json
import pandas as pd
all_files = os.listdir('/comment')
all_files = os.listdir('/Users/weiwei/Documents/comment')
all_paths = []
contents = []

all_files = [f for f in os.listdir('/Users/weiwei/Documents/comment')]
for i in all_files:
    all_paths.append(os.path.join('./comment/', i))


for path in all_paths:
    with open(path, encoding = 'unicode_escape') as f:
        contents.append(f.read())



import json
import jsonpath
import pandas as pd
comment_file = json.load(open('/Users/weiwei/Documents/comment/Blogger case 1 comments.json', 'r', encoding='utf-8'))
comment_content = jsonpath.jsonpath(comment_file, '$..content')
user_name = jsonpath.jsonpath(obj, '$..user_info[nickname]')

maincomments = jsonpath.jsonpath(obj, '$.data.comments[*].content')
maincommenters = jsonpath.jsonpath(obj, '$..data.comments[*].user_info[nickname]')
maincomment_like = jsonpath.jsonpath(obj, '$..data.comments[*].like_count')


#提取评论的日期，并转换成正确日期格式
import datetime
maincomment_jason_time = jsonpath.jsonpath(obj, '$..data.comments[*].create_time')
timestamps = maincomment_jason_time
# convert timestamps to datetime objects with hours, minutes, and seconds
maincomment_datetimes = []
for ts in maincomment_jason_time:
    dt = datetime.datetime.fromtimestamp(ts/1000.0)
    maincomment_datetimes.append(dt)
# convert datetimes to strings with format YYYY-MM-DD HH:MM:SS
maincomment_time = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in maincomment_datetimes]
# print list of datetime strings
print(maincomment_time)


#如果我只想要日期就用这个
import datetime
timestamps = [1658680087000, 1658485454000, 1658483585000, 1658464159000, 1658481345000, 1658587411000, 1658755302000, 1658651347000, 1658650123000, 1658907096000]
# convert timestamps to datetime objects and keep only year, month, and date
dates = [datetime.datetime.fromtimestamp(ts/1000.0).date() for ts in timestamps]
# print dates
for d in dates:
    print(d)
