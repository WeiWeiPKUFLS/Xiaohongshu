import json
import pandas as pd
from datetime import datetime

#打开本地的json文件
#1要改地址
with open('/Users/weiwei/Documents/comment/Blogger case 2 comments.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#提取评论的内容
comments = []
for comment in data['data']['comments']:
    sub_comments_list = []
    for sub_comment in comment.get('sub_comments', []):
        sub_create_time = datetime.fromtimestamp(sub_comment['create_time'] // 1000)
        sub_like_count = sub_comment.get('like_count', None)
        sub_comments_list.append([sub_comment['content'], 
                                  sub_comment['user_info']['nickname'], 
                                  sub_create_time.strftime("%d/%m/%Y %H:%M"),sub_like_count])
        
    create_time = datetime.fromtimestamp(comment['create_time'] // 1000)
    like_count = comment.get('like_count', None)
    comments.append([comment['content'], 
                     comment['user_info']['nickname'], 
                     create_time.strftime("%d/%m/%Y %H:%M"),
                     like_count,
                     sub_comments_list])

# 存进一个DataFrame里面
df = pd.DataFrame(comments, columns=['content', 'nickname', 'create_time', 'like_count', 'sub_comments'])

# 保存为txt文件
#2要改地址
with open('/Users/weiwei/Documents/comment/Blogger case 2.txt', 'a', encoding='utf-8') as f:
    for i, row in df.iterrows():
        f.write(f"{i+1}. {row['content']}\n")
        f.write(f"   Posted by: {row['nickname']} on {row['create_time']},")
        if not pd.isna(row['like_count']):
            f.write(f" Likes: {row['like_count']}\n")
        if not row['sub_comments']:
            f.write("   No sub-comments\n")
        else:
            f.write("   Sub-comments:\n")
            for j, sub_comment in enumerate(row['sub_comments']):
                f.write(f"     {j+1}. {sub_comment[0]} \n")
                f.write(f"         Posted by: {sub_comment[1]} on {sub_comment[2]}, Likes: {sub_comment[3]}\n")
        f.write("\n")



#如果我只想要日期就用这个
import datetime
timestamps = [1658680087000, 1658485454000, 1658483585000, 1658464159000, 1658481345000, 1658587411000, 1658755302000, 1658651347000, 1658650123000, 1658907096000]
# convert timestamps to datetime objects and keep only year, month, and date
dates = [datetime.datetime.fromtimestamp(ts/1000.0).date() for ts in timestamps]
# print dates
for d in dates:
    print(d)
    
    
#批量处理文件
import os
import json
import pandas as pd
from datetime import datetime

# set the directory path记得改地址
directory = "/Users/weiwei/Documents/Participant notes/Zhichuantao/Zhichuantao video"

# loop through all the json files in the directory
for file in os.listdir(directory):
    if file.endswith("comments.json"):
        # extract the file name of the txt file
        txt_file_name = file.split("comments")[0].strip() + ".txt"
        # create the full path for both the json and txt files
        json_file_path = os.path.join(directory, file)
        txt_file_path = os.path.join(directory, txt_file_name)

        # extract the comments data from the json file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        comments = []
        for comment in data['data']['comments']:
            sub_comments_list = []
            for sub_comment in comment.get('sub_comments', []):
                sub_create_time = datetime.fromtimestamp(sub_comment['create_time'] // 1000)
                sub_like_count = sub_comment.get('like_count', None)
                sub_comments_list.append([sub_comment['content'], 
                                          sub_comment['user_info']['nickname'], 
                                          sub_create_time.strftime("%d/%m/%Y %H:%M"),sub_like_count])
                
            create_time = datetime.fromtimestamp(comment['create_time'] // 1000)
            like_count = comment.get('like_count', None)
            comments.append([comment['content'], 
                             comment['user_info']['nickname'], 
                             create_time.strftime("%d/%m/%Y %H:%M"),
                             like_count,
                             sub_comments_list])

        # save the comments data to a txt file
        df = pd.DataFrame(comments, columns=['content', 'nickname', 'create_time', 'like_count', 'sub_comments'])
        with open(txt_file_path, 'a', encoding='utf-8') as f:
            for i, row in df.iterrows():
                f.write(f"{i+1}. {row['content']}\n")
                f.write(f"   Posted by: {row['nickname']} on {row['create_time']},")
                if not pd.isna(row['like_count']):
                    f.write(f" Likes: {row['like_count']}\n")
                if not row['sub_comments']:
                    f.write("   No sub-comments\n")
                else:
                    f.write("   Sub-comments:\n")
                    for j, sub_comment in enumerate(row['sub_comments']):
                        f.write(f"     {j+1}. {sub_comment[0]} \n")
                        f.write(f"         Posted by: {sub_comment[1]} on {sub_comment[2]}, Likes: {sub_comment[3]}\n")
                f.write("\n")


