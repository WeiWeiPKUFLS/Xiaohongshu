#!use python3 to launch it
# encoding: utf-8

import bs4
from bs4 import BeautifulSoup
import requests
import os
import sys
import urllib.request
non_bmp_map = dict.fromkeys(range(0x10000,sys.maxunicode + 1),0xfffd)
f = open('/Users/weiwei/Documents/comment/Blogger case 1.txt','a',encoding='utf-8')

#引入离线的网页
soup = BeautifulSoup(open("/Users/weiwei/Documents/Blogger case 1.html"), features="html.parser")
#抽取笔记的标题
title = soup.find('div', class_ = 'note-content').find('div', class_ = 'title').get_text()
f.write('Title: '+ title + '\n' + '\n')
#抽取笔记正文
content = soup.find('div', class_ = 'note-content').find('div', class_ = 'desc').get_text('\n','<br>')
f.write('Main text: '+ content + '\n' + '\n')
#抽取hashtags
hashtags = soup.find(attrs={"name":"keywords"})['content']
f.write('Hashtags: ' + hashtags + '\n' + '\n')

#抽取发布时间
publishdate = soup.find('div', class_ = 'date').get_text()
f.write('Publishdate: ' + publishdate + '\n' + '\n')
f.close()




#对于图文笔记
#抽取图片链接
urls = []
for div in soup.find_all("div", class_="swiper-slide zoom-in"):
    style_attr = div.get("style")
    url = style_attr.split("(")[-1].split(")")[0]
    urls.append(url)
print(urls)
#下载图片并保存
for i, url in enumerate(urls):
    response = requests.get(url)
    filename = f"/Users/weiwei/Documents/comment/Blogger case 1 - {i+1}.jpg"
    with open(filename, 'wb') as f:
        f.write(response.content)

	
	
#对于视频笔记	
#找到要抽取视频和视频缩略图的那个部分作为script_text
script_element = soup.select_one('body > script:nth-child(3)')
script_text = script_element.string

#抽取视频并保存
json_str = script_text.split("window.__INITIAL_STATE__=")[1]
pattern = r'"backupUrls":\s*\[([\s\S]*?)\]'
backup_urls_str = re.search(pattern, json_str).group(1)
first_backup_url = backup_urls_str.strip('"').split(',')[0].strip().rstrip('"')

decoded_url = urllib.parse.unquote(first_backup_url)
decoded_url = first_backup_url.encode().decode('unicode_escape')
decoded_url = decoded_url.replace('\\', '')
print(decoded_url)

response1 = requests.get(decoded_url)
with open('/Users/weiwei/Documents/comment/Blogger case 2 video.mp4', 'wb') as f:
    f.write(response1.content)

#抽取视频缩略图的链接
for match in re.finditer('"url":"(.*?)"',script_text):
    image_url = match.group(1).encode().decode('unicode_escape')
    print(image_url)
response2 = requests.get(image_url)
with open('/Users/weiwei/Documents/comment/Blogger case 2 videothumbnail.jpg', 'wb') as f:
	f.write(response2.content)	
	
	


#批量处理同一个文件夹的内容	
#图文笔记
import os
import sys
import urllib.request
from datetime import datetime
import bs4
import requests
from bs4 import BeautifulSoup

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# directory where the HTML files are stored记得改地址
directory = "/Users/weiwei/Documents/Participant notes/Pax/Pax photo-text"

# loop through all the HTML files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        html_file = os.path.join(directory, filename)
        txt_file = os.path.splitext(html_file)[0] + ".txt"
        image_directory = directory

        # open the HTML file and create a BeautifulSoup object
        with open(html_file, encoding='utf-8') as f:
            soup = BeautifulSoup(f, features="html.parser")

        # extract the note title, main text, hashtags, and publish date
        title = soup.find('div', class_='note-content').find('div', class_='title').get_text()
        content = soup.find('div', class_='note-content').find('div', class_='desc').get_text('\n', '<br>')
        hashtags = soup.find(attrs={"name": "keywords"})['content']
        date = soup.find('div', class_='date').get_text()
        
        # handle different date formats
        try:
            formatdate = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            formatdate = datetime.strptime('2023-' + date, '%Y-%m-%d')
        
        publishdate = formatdate.strftime('%d/%m/%Y')

        # write the extracted data to the corresponding txt file
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write('Title: ' + title + '\n\n')
            f.write('Main text: ' + content + '\n\n')
            f.write('Hashtags: ' + hashtags + '\n\n')
            f.write('Publishdate: ' + publishdate + '\n\n')

        # extract the image URLs and download the images
        urls = []
        for div in soup.find_all("div", class_="swiper-slide zoom-in"):
            style_attr = div.get("style")
            url = style_attr.split("(")[-1].split(")")[0]
            urls.append(url)

        for i, url in enumerate(urls):
            response = requests.get(url)
            filename = os.path.splitext(os.path.basename(html_file))[0] + f" - {i+1}.jpg"
            filename = os.path.join(image_directory, filename.replace("--", "-"))
            with open(filename, 'wb') as f:
                f.write(response.content)

        f.close()



#视频笔记
import os
import re
import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup


# Define the input and output directories改地址
input_dir = "/Users/weiwei/Documents/Participant notes/Xueer/Xueer video"
output_dir = "/Users/weiwei/Documents/Participant notes/Xueer/Xueer video"

# Loop through all the HTML files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".html"):
        # Create the file paths for the HTML, text, video, and thumbnail image files
        html_filepath = os.path.join(input_dir, filename)
        text_filepath = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
        video_filepath = os.path.join(output_dir, os.path.splitext(filename)[0] + ".mp4")
        thumbnail_filepath = os.path.join(output_dir, os.path.splitext(filename)[0] + "_thumbnail.jpg")

        # Open the HTML file with BeautifulSoup
        with open(html_filepath, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Extract the note title, content, hashtags, and publish date
        title = soup.find("div", class_="note-content").find("div", class_="title").get_text()
        content = soup.find("div", class_="note-content").find("div", class_="desc").get_text("\n", "<br>")
        hashtags = soup.find(attrs={"name": "keywords"})["content"]
        publishdate = soup.find("div", class_="date").get_text()

        # Write the note title, content, hashtags, and publish date to a text file
        with open(text_filepath, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n\n")
            f.write(f"Main text: {content}\n\n")
            f.write(f"Hashtags: {hashtags}\n\n")
            f.write(f"Publishdate: {publishdate}\n\n")

        # Extract the video URL from the HTML file
        script_element = soup.select_one("body > script:nth-child(3)")
        script_text = script_element.string
        json_str = script_text.split("window.__INITIAL_STATE__=")[1]
        pattern = r'"backupUrls":\s*\[([\s\S]*?)\]'
        backup_urls_str = re.search(pattern, json_str).group(1)
        first_backup_url = backup_urls_str.strip('"').split(",")[0].strip().rstrip('"')
        decoded_url = urllib.parse.unquote(first_backup_url)
        decoded_url = first_backup_url.encode().decode("unicode_escape")
        decoded_url = decoded_url.replace("\\", "")

        # Download the video and save it to a file
        response = requests.get(decoded_url)
        with open(video_filepath, "wb") as f:
            f.write(response.content)

        # Extract the video thumbnail URL from the HTML file
        for match in re.finditer('"url":"(.*?)"', script_text):
            image_url = match.group(1).encode().decode("unicode_escape")

        # Download the video thumbnail and save it to a file
        response = requests.get(image_url)
        with open(thumbnail_filepath, "wb") as f:
            f.write(response.content)


	
	
	
	
	
	


#抽取评论(需要对应用户，时间，然后还有下属的评论)
#comments = []
#replies = soup.find('div', class_='all-tip').find_all('p', class_='content')
#for reply in replies:
#    comment = reply.text
#    print(comment)
#    comments.append(comment)
#commenters = []
#usernames = soup.find_all('h4', class_="user-nickname")
#for i in usernames:
#    name = i.text
#    nam = name.translate(non_bmp_map) + ':'
#    print (nam)
#    commenters.append(nam)
#commenttimes = []
#replytimes = soup.find_all('span', class_="publish-time")
#for replytime in replytimes:
#    commenttime = replytime.text
#    print(commenttime)
#    commenttimes.append(commenttime)
#import pandas as pd
#commentdata = pd.DataFrame({'commenters':commenters,'comments':comments, 'comment-time': commenttimes})
#commentdata.to_csv('Blogger A self-selected note 7 text.txt',index=False,encoding='utf_8_sig', mode='a')

#处理评论的评论
#subcomments = []
#subcommenters = []
#subreplies = soup.find('div', class_='all-tip').find_all('p', class_='reply-content')
#for subreply in subreplies:
#    subrep = subreply.text
#    print(subrep)
#    subcomments.append(subrep)

#subrepliers = soup.find('div', class_='all-tip').find_all('span', class_='replier')
#for subreplier in subrepliers:
#    suber = subreplier.text
#    print(suber)
#    subcommenters.append(suber)
#subcommentdata = pd.DataFrame({'subcommenters': subcommenters,'subcomments': subcomments})
#subcommentdata.to_csv('Blogger A self-selected note 7 text.txt',index=False,encoding='utf_8_sig', mode='a')

#视频下载
#videoSrc = soup.find('div', class_ = 'videoframe').find('video').get('src')
#urllib.request.urlretrieve(videoSrc,'Blogger A self-selected note 7.mp4')
#抽取video transcript
#f2 = open('Blogger A self-selected note 7 transcript.txt', 'a', encoding='utf-8')
#transcript = soup.find('p', class_ = 'generated-text').get_text()
#f2.write('(transcript)' + transcript + '\n')
#f2.close()

#抽取视频
#videoSrc = soup.find('div', class_ = 'videoframe').find('video').get('src')
#urllib.request.urlretrieve(videoSrc,'participant 1 self-selected 7.mp4')

#抽取视频transcript
#f2 = open('participant 1 self-selected note 7 transcript.txt', 'a', encoding='utf-8')
#transcript = soup.find('p', class_ = 'generated-text').get_text()
#f2.write('(transcript)' + transcript + '\n')
#f2.close()

#抽取图片
#image = soup.find('div', class_ = 'inner').find_all('style')
#抽取图片的链接
#picUrls = []
#pics = soup.find('div', class_ = 'small-pic').find_all('div')
#for pic in pics:
#   picUrl = 'http:' + pic.find('i', class_ = 'img').get('style')[21:-32]
#    picUrls.append(picUrl)
#for i in picUrls:
#	image_url = "'http://' + i"
#	headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
#	r = requests.get(image_url,headers=headers)
#	f = open("i.jpg", 'wb')
#	f.write(r.content)
#	f.close()

#直接从相关链接下载图片（要补充http://，是不是可以‘http://’+'抽取出来的链接')
#image_url='http://ci.xiaohongshu.com/5b123788-3c47-8610-e910-a37c6dc3be4f?imageView2/2/w/1080/format/jpg'
#headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
#r = requests.get(image_url,headers=headers)

#默认放进Documents(还需要改具体存放地址)
f = open("1.jpg",'wb')
f.write(r.content)
f.close()


#试一下用xpath
#from lxml import etree
#maintext = soup.find('div', class_ = 'content')
#tree = etree.HTML(maintext)
#li_list = tree.xpath('//div[@class="content"]/p')
#fp = open('test1.txt','w',encoding='utf-8')
#for li in li_list:
	#paragraph = li.xpath('./div[2]//h3/text()')[0] + li.xpath('./div[2]/div[2]/p/span/text()')[0]


#a = soup.find_all('span', class_="username")



#这里开始抓取网页
#req=requests.get('https://www.crrcgo.cc/admin/crr_supplier.html?page=1')
#req.encoding = "utf-8"
#html=req.text
#soup = BeautifulSoup(req.text,features="html.parser")
# url = "这里要补具体笔记链接"
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
# response = requests.get(url=url,headers=headers)
# content = response.text
# print(content)
#notetitle=soup.find_all('div',class_="title")
#keyword = soup.find(attrs={"name":"keywords"})['content']
#反反爬虫
#ua = UserAgent(use_cache_server=False)
#headers={"User-Agent": a}
#res=requests.get(url,headers=headers)
#t=res.text
#print(t)



#text = soup.find('div', class_ = 'content').get_text()
#只能抽到第一段
#notetext = soup.find('div', class_ = 'content').find('p').get_text()
#抽取出来包含分段</p>的正文
#notetext = soup.find('div', class_ = 'content').find_all('p')
