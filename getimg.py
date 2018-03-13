import re
import urllib.request
from bs4 import BeautifulSoup  

#爬取网页html
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


html = getHtml("http://sports.ifeng.com/a/20180208/55880522_0.shtml")
html = html.decode('UTF-8')

def getcontent(html):
    soup = BeautifulSoup(html, 'html.parser')  
    main_content = soup.find('div', {'id': 'artical_real'})
    return main_content
    
#获取图片链接的方法
def getImg(article):
    # 利用正则表达式匹配网页里的图片地址
    reg = r'src="([.*\S]*\.jpg)"'
    imgre=re.compile(reg)
    imglist=re.findall(imgre,str(article))
    return imglist
content = getcontent(html)
print(content)

imgList=getImg(content)
imgCount=0
#for把获取到的图片都下载到本地pic文件夹里，保存之前先在本地建一个pic文件夹
for imgPath in imgList:
    f=open(str(imgCount)+".jpg",'wb')
    f.write((urllib.request.urlopen(imgPath)).read())
    f.close()
    imgCount+=1
print("全部抓取完成")
