#coding: utf-8  
  
import codecs  
from urllib import request, parse  
from bs4 import BeautifulSoup  
import re  
import time  
from urllib.error import HTTPError, URLError  
import sys  
import os
import importlib

import urllib.request

importlib.reload(sys)
###新闻类定义  
class News(object):  
    def __init__(self):  
        self.url = None  #该新闻对应的url  
        self.topic = None #新闻标题  
        self.date = None #新闻发布日期  
        self.content = None  #新闻的正文内容  
        self.author = None  #新闻作者  

def getImg(article):
    # 利用正则表达式匹配网页里的图片地址
    reg = r'src="([.*\S]*\.jpg)"'
    imgre=re.compile(reg)
    imglist=re.findall(imgre,str(article))
    return imglist

def getImg2(article):
    # 利用正则表达式匹配网页里的图片地址
    reg = r'src="([.*\S]*\.jpeg)"'
    imgre=re.compile(reg)
    imglist=re.findall(imgre,str(article))
    return imglist

def is_chinese(uchar):
    if uchar >= u'\u2E80' and uchar <= u'\uFE4F':
        return True
    else:
        return False

###如果url符合解析要求，则对该页面进行信息提取  
def getNews(url):  
    
    global count
    
    url2 = str()
    for ch in url:
        if is_chinese(ch):
            ch = quote(ch)
        url2 += ch    
    url = url2
    
    #获取页面所有元素  
    html = request.urlopen(url).read().decode('utf-8', 'ignore')
    
    
    #解析  
    soup = BeautifulSoup(html, 'html.parser')  
  
    #获取信息  
      
      
    news = News()  #建立新闻对象  
    
    #if not(soup.find('div', {'id': 'main_content'})): return   
    #main_content = soup.find('div', {'id': 'main_content'})   #新闻正文内容 
    
    
    if not(soup.find('div', {'id': 'artical_real'})): return   
    main_content = soup.find('div', {'id': 'artical_real'})   #新闻正文内容 
      
    imgList = getImg(main_content)
    imgList2 = getImg2(main_content)
    content = ''  
      
    for p in main_content.select('p'):  
        content = content + p.get_text()
        if len(content) > 200:
            break
  
    news.content = content  
  
    news.url = url       #新闻页面对应的url  
    
    if (os.path.exists('data/')==False):
        os.mkdir('data/')
    
    path = ('data/%d/') % count
    if (os.path.exists(path)==False):
        os.mkdir(path)
    
    path_text = ('data/%d/text.txt') % count
    path_url = ('data/%d/url.txt') % count
    text_out =  open(path_text, 'w', encoding='utf-8')  
    url_out = open(path_url, 'w', encoding='utf-8') 
    
    
    text_out.write(news.content+'\n')  
    url_out.write(url+'\n')
    
    imgCount=0
    for imgPath in imgList:
        f=open("data/"+str(count)+"/"+str(imgCount)+".jpg",'wb')
        f.write((urllib.request.urlopen(imgPath)).read())
        f.close()
        imgCount+=1
    
    
    
    imgCount=0
    for imgPath in imgList2:
        f=open("data/"+str(count)+"/"+str(imgCount)+".jpeg",'wb')
        f.write((urllib.request.urlopen(imgPath)).read())
        f.close()
        imgCount+=1
    count += 1
    
    
    
  
##dfs算法遍历全站###  
def dfs(url):  
    global local
    pattern1 = 'http://tech\.ifeng\.com\/[a-z0-9_\/\.]*$'     #可以继续访问的url规则  
    pattern2 = 'http://tech\.ifeng\.com\/a\/[0-9]{8}\/[0-9]{8}\_0\.shtml$'  #解析新闻信息的url规则  
  
    #该url访问过，则直接返回  
    if url in visited:  return  
    print(count,' --- ',url)  
  
    #把该url添加进visited()  
    visited.add(url)  
    # print(visited)  
  
    try:  
        #该url没有访问过的话，则继续解析操作  
        html = request.urlopen(url).read().decode('utf-8', 'ignore')  
        # print(html)  
        soup = BeautifulSoup(html, 'html.parser')  
  
        if re.match(pattern2, url): 
            getNews(url)  
  
        ####提取该页面其中所有的url####  
        links = soup.findAll('a', href=re.compile(pattern1))  
        for link in links:  
            print(link['href'])  
            if link['href'] not in visited:   
                dfs(link['href'])  
                # count += 1  
    except URLError as e:  
        print(e)  
        return  
    except HTTPError as e:  
        print(e)  
        return  
    # print(count)  
    # if count > 3: return  
  
visited = set()  ##存储访问过的url  
count = 0
#f = open('ifeng/news.txt', 'a+', encoding='utf-8')  
#furl = open('ifeng/urls.txt', 'a+', encoding='utf-8')  
dfs('http://tech.ifeng.com/')  
