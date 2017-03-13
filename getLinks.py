# -*- coding:utf-8 -*-
import os,urllib,urllib2,re
from bs4 import BeautifulSoup
import time
import sys

#所需变量初始化及准备工作
#记录程序开始时间
start = time.clock()
#设置网站首页地址
rooturl='http://www.lovefou.com'
#创建一个list用于保存课程大类的链接地址
indexlist=[]
outpath = "/Users/daiguojin/lovefou2/"
#header = {'Connection' : 'keep-alive','User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0' } 

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

##====================以下为方法========================##

'''
方法名：getContent
作用：从pagelist中的url中解析出相关内容，并保存到本地文本中
参数：含有具体课程内容的网址:w 
'''
def getContent(url = ''):
    for i in range(1,79):
        print 'page:{0}'.format(i)
        
        url = '{0}/dongtaitu/list_{1}.html'.format(rooturl,i)
        print url
        req = urllib2.Request(url, headers=header)
        currentPage=urllib2.urlopen(req).read().decode('utf8')
        currentText=BeautifulSoup(currentPage, "html.parser") #利用bs进行解析
        links=currentText.find('div',{'class':'lovefou'}).findAll('p')
        for l in links:
            #以标题为文件名，创建txt文件，并写入正文内容
            f=open('lovefou.txt','a')
            f.write(l.find("a").get('href') + '\n')
            f.close()
            print url


def report(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r%d%%" % percent + ' complete')
    sys.stdout.flush()

def download(imgList, page):
    x = 1
    for imgurl in imgList:
        filepathname=str(outpath+'pic_%09d_%010d'%(page,x)+str(os.path.splitext(urllib2.unquote(imgurl).decode('utf8').split('/')[-1])[1])).lower()
        print 'Download file :'+ imgurl+' >> '+filepathname
        urllib.urlretrieve(imgurl,filepathname)
        x+=1

if __name__ == '__main__':
#    getContent()
    f=file('lovefou.txt')
    page = 1
    while True: 
        line=f.readline() 
        if len(line)==0: # Zero length indicates EOF 
            break 
        url = '{0}{1}'.format(rooturl,line)
        req = urllib2.Request(url, headers=header)
        currentPage=urllib2.urlopen(req).read() #读取源码
        currentText=BeautifulSoup(currentPage, "html.parser") #利用bs进行解析
        image=currentText.find('div',{'class':'dongtai'}).find('img').get('src')
        filepathname=str(outpath+'pic_%09d'%(page)+str(os.path.splitext(urllib2.unquote(image).decode('utf8').split('/')[-1])[1])).lower()

        print filepathname

        request = urllib2.Request(image,headers=header)  
        response = urllib2.urlopen(request)  
        imageContents = response.read()  
        sys.stdout.write('\rFetching ' + image + '\n')
        try:
            f1 = open(filepathname, 'wb')  
            f1.write(imageContents)  
            f1.close()  
        except Exception as e:
            print 'error'

#            urllib.urlretrieve(image,filepathname,reporthook=report)
        sys.stdout.write("\rDownload complete, saved as %s" % (filepathname) + '\n\n')
        sys.stdout.flush()
        page = page + 1
        time.sleep(2)
    f.close() 
    print 'end'
