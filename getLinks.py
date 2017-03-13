# -*- coding:utf-8 -*-
import os,urllib,urllib2,re
from bs4 import BeautifulSoup
import time
import sys

#���������ʼ����׼������
#��¼����ʼʱ��
start = time.clock()
#������վ��ҳ��ַ
rooturl='http://www.lovefou.com'
#����һ��list���ڱ���γ̴�������ӵ�ַ
indexlist=[]
outpath = "/Users/daiguojin/lovefou2/"
#header = {'Connection' : 'keep-alive','User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0' } 

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

##====================����Ϊ����========================##

'''
��������getContent
���ã���pagelist�е�url�н�����������ݣ������浽�����ı���
���������о���γ����ݵ���ַ:w 
'''
def getContent(url = ''):
    for i in range(1,79):
        print 'page:{0}'.format(i)
        
        url = '{0}/dongtaitu/list_{1}.html'.format(rooturl,i)
        print url
        req = urllib2.Request(url, headers=header)
        currentPage=urllib2.urlopen(req).read().decode('utf8')
        currentText=BeautifulSoup(currentPage, "html.parser") #����bs���н���
        links=currentText.find('div',{'class':'lovefou'}).findAll('p')
        for l in links:
            #�Ա���Ϊ�ļ���������txt�ļ�����д����������
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
        currentPage=urllib2.urlopen(req).read() #��ȡԴ��
        currentText=BeautifulSoup(currentPage, "html.parser") #����bs���н���
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
