#!use python3 to launch it
# encoding: utf-8

import bs4
from bs4 import BeautifulSoup
import requests
import sys
import urllib.request
non_bmp_map = dict.fromkeys(range(0x10000,sys.maxunicode + 1),0xfffd)
f = open('mainnote2.txt','a',encoding='utf-8')

#引入离线的网页
soup = BeautifulSoup(open("/Users/weiwei/Documents/test webscraping/2.html"))
#抽取笔记的标题
title = soup.find('div', class_ = 'note-top').find('h1', class_ = 'title').get_text()
f.write('(title)'+ title + '\n')
#抽取笔记正文
paragraphs = []
notetext = soup.find('div', class_ = 'content').find_all('p')
for note in notetext:
    para = note.text
    paragraphs.append(para)
for pp in paragraphs:
	f.write(pp + '\n') 
#抽取发布时间
publishdate = soup.find('div', class_ = 'publish-date').get_text()
f.write('(publishdate)' + publishdate + '\n')

f.close()

#抽取评论(需要对应用户，时间，然后还有下属的评论)
comments = []
replies = soup.find('div', class_='all-tip').find_all('p', class_='content')
for reply in replies:
    comment = reply.text
    print(comment)
    comments.append(comment)
for cc in comments:
	f.write('(top5comments)' + cc + '\n')

usernames = soup.find_all('h4', class_="user-nickname")
commenters = []
for i in usernames:
    name = i.text
    nam = name.translate(non_bmp_map)
    print (nam)
    commenters.append(nam)

#对应评论和评论者
import pandas as pd
commentdata = pd.DataFrame({'commenters':commenters,'comments':comments})
commentdata.to_csv('participant 1 self-selected note 7 comment data.csv',index=False,encoding='utf_8_sig')




#抽取视频
videoSrc = soup.find('div', class_ = 'videoframe').find('video').get('src')
urllib.request.urlretrieve(videoSrc,'participant 1 self-selected 7.mp4')

#抽取视频transcript
f2 = open('participant 1 self-selected note 7 transcript.txt', 'a', encoding='utf-8')
transcript = soup.find('p', class_ = 'generated-text').get_text()
f2.write('(transcript)' + transcript + '\n')
f2.close()

#抽取图片
image = soup.find('div', class_ = 'inner').find_all('style')
#抽取图片的链接
picUrls = []
pics = soup.find('div', class_ = 'small-pic').find_all('div')
for pic in pics:
    picUrl = 'http:' + pic.find('i', class_ = 'img').get('style')[21:-32]
    picUrls.append(picUrl)
for i in picUrls:
	image_url = "'http://' + i"
	headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
	r = requests.get(image_url,headers=headers)
	f = open("i.jpg", 'wb')
	f.write(r.content)
	f.close()

#直接从相关链接下载图片（要补充http://，是不是可以‘http://’+'抽取出来的链接')
image_url='http://ci.xiaohongshu.com/5b123788-3c47-8610-e910-a37c6dc3be4f?imageView2/2/w/1080/format/jpg'
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
r = requests.get(image_url,headers=headers)

#默认放进Documents(还需要改具体存放地址)
f = open("1.jpg",'wb')
f.write(r.content)
f.close()


#试一下用xpath
from lxml import etree
maintext = soup.find('div', class_ = 'content')
tree = etree.HTML(maintext)
li_list = tree.xpath('//div[@class="content"]/p')
fp = open('test1.txt','w',encoding='utf-8')
for li in li_list:
	paragraph = li.xpath('./div[2]//h3/text()')[0] + li.xpath('./div[2]/div[2]/p/span/text()')[0]


a = soup.find_all('span', class_="username")



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
