# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#������վ��ҳ��ַ
rooturl='http://www.cecepa.com/artkt/'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}


urlList=[]
titleList=[]

#��ʼ��ȡ
# 1���Ƚ�����Ŀ¼����ȡ13��Ŀ������
print('������Ŀ¼')

request = urllib2.Request(rooturl,headers = header)  
rawtext=urllib2.urlopen(request).read()
soup = BeautifulSoup(rawtext, 'lxml')
targetDiv=soup.find('ul',{'class':'list'})

catalogLinks=targetDiv.findAll('li')
for i in catalogLinks:
    title = i.find('span',{'class':'n'}).get_text();
    if "��Ϸ����ͬ��CG".decode('gbk').encode("utf-8") in title:
        titleList.append(title)
        urlList.append(i.find('a').get('href'))

f=open('F:/1.txt','w+')
for i in range(len(urlList)):
	f.write(urlList[i]+'     '+titleList[i]+'\r\n')
f.close()