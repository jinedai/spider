# -*- coding: utf-8 -*-  
#!/usr/bin/python  
#---------------------------------------  
#   ����MM����  
#   �汾��0.1  
#   ���ߣ�fantasy  
#   ���ڣ�2014-06-05  
#   ���ԣ�Python 2.7  
#   ���ܣ�����վ��ͼƬ���ݷ�Ŀ¼�洢������  
#----------------------------------------  
  
import string  
import urllib2  
import urllib  
import re  
from threading import Thread  
from Queue import Queue  
from time import sleep  
import os  
import sys  
  
#Q���������(Ԫ�����ÿ����)  
#thread_num�ǲ����߳�����  
Q = Queue()  
thread_num = 7  
  
  
#----------- ����ҳ���ϵĸ��ֱ�ǩ -----------  
class HTML_Tool:  
    # �÷� ̰��ģʽ ƥ�� \t ���� \n ���� �ո� ���� ������ ���� ͼƬ  
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")  
      
    # �÷� ̰��ģʽ ƥ�� ����<>��ǩ  
    EndCharToNoneRex = re.compile("<.*?>")  
  
    # �÷� ̰��ģʽ ƥ�� ����<p>��ǩ  
    BgnPartRex = re.compile("<p.*?>")  
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")  
    CharToNextTabRex = re.compile("<td>")  
  
    # ��һЩhtml�ķ���ʵ��ת��Ϊԭʼ����  
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]  
      
    def Replace_Char(self,x):  
        x = self.BgnCharToNoneRex.sub("",x)  
        x = self.BgnPartRex.sub("\n    ",x)  
        x = self.CharToNewLineRex.sub("\n",x)  
        x = self.CharToNextTabRex.sub("\t",x)  
        x = self.EndCharToNoneRex.sub("",x)  
  
        for t in self.replaceTab:    
            x = x.replace(t[0],t[1])    
        return x    
#----------- ����ҳ���ϵĸ��ֱ�ǩ -----------    
  
  
class MM_Spider:  
    # ���캯��  
    def __init__(self,url):  
        self.myUrl=url  
        self.urlNum=0  
        self.myTool = HTML_Tool()   
  
    #headerαװ���html����  
    def get_html(self,url):  
        req_header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
        req_timeout = 20  
        try:  
            req = urllib2.Request(url,None,req_header)  
            page = urllib2.urlopen(req,None,req_timeout)  
            html = page.read().decode("utf-8")  
        except urllib2.URLError as e:  
            print e.message  
        except socket.timeout as e:  
            user_html(self.myUrl)  
        return html  
  
  
    #ÿ���߳�ȥץһ���˵�ͼ�����ȣ�Ҫ�Լ���֯�ļ�Ŀ¼  
    def working(self):  
        while True:  
            url=Q.get()  
            self.get_MM_pic(url)  
            #sleep(1)  
            Q.task_done()  
              
    def get_MM_pic(self,url):  
        personal_page=self.get_html(url)  
        #<title>��Ů�r�� | ��Ůͼ�� ���� ��ŮͼƬ ��Ůд��</title>  
        title=re.search(r'<title>([^ |]*)',personal_page,re.S)  
        print title.group(1)  
        os.mkdir(title.group(1))  
        #<div class="column grid_12" style="margin-bottom: 10px">  
        #</div>  
        profile=re.search(r'<div class="column grid_12" style="margin-bottom: 10px">([^<]*)',personal_page,re.S)  
          
        f = open(title.group(1)+'/'+title.group(1)+'���'+'.txt','w+')  
        if profile==None:  
            f.writelines("no profile")  
        else:  
            f.writelines(self.myTool.Replace_Char(profile.group(1)))  
        f.close()  
         #<div class="grid_title">  
        #<a href='http://girl-atlas.com/a/10140314061500000191' class="caption">[NS Eyes] #184 Sayaka Isoyama ��ɽ���䤫</a>  
        #</div>  
        album=re.findall(r'<a href=\'([^\']*)\' class="caption">',personal_page,re.S)  
        count=0  
        for item in album:  
            print item  
            #raw_input()  
            count=self.save_MM_page(item,title.group(1),count)  
  
  
    def save_MM_page(self,url,catalog,count):  
        photos_page=self.get_html(url)  
        #<img title="2011 Girls Generation��Holiday��1st Part - No. 24 - 24" delay='http://girlatlas.b0.upaiyun.com/45/20121223/0041f70328b00e5535e2.jpg!mid' />  
        photos=re.findall(r"<img title=.*?delay='(.*?)' />",photos_page,re.S)  
        for item in photos:  
            urllib.urlretrieve(item,catalog+ '/'+'%d.jpg' %count)  
            #print catalog  
            count+=1  
        return count  
              
              
    #������  
    def MM_pic(self):  
        #���ñ���
        reload(sys)  
        sys.setdefaultencoding('utf8')  
        #�л�Ŀ¼  
        os.chdir('pics')  
        #׼���̳߳�  
        for i in range(thread_num):  
            t=Thread(target=self.working)  
            t.setDaemon(True)  
            t.start()  
        #�������з�������  
        myPage=self.get_html(self.myUrl).encode('GB18030')
        #<li title='�ɽ���䤫' tid='10' length='13'><a target="_blank" href="http://girl-atlas.com/t/10">�ɽ���䤫</a></li>  
        myItems=re.findall('<div class="tab" tid=".*?><a href="([^"]*)">',myPage,re.S)  
        print myItems

        for item in myItems:  
            Q.put(item)  
            self.urlNum+=1  
            print item  
        print self.urlNum  
  
raw_input()
url='http://girl-atlas.com/'  
mySpider=MM_Spider(url)  
mySpider.MM_pic()  
  
Q.join()  
