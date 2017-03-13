# -*- coding: utf-8 -*-  
#!/usr/bin/python  
#---------------------------------------  
#   程序：MM爬虫  
#   版本：0.1  
#   作者：fantasy  
#   日期：2014-06-05  
#   语言：Python 2.7  
#   功能：将网站的图片内容分目录存储到本地  
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
  
#Q是任务队列(元素针对每个人)  
#thread_num是并发线程总数  
Q = Queue()  
thread_num = 7  
  
  
#----------- 处理页面上的各种标签 -----------  
class HTML_Tool:  
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片  
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")  
      
    # 用非 贪婪模式 匹配 任意<>标签  
    EndCharToNoneRex = re.compile("<.*?>")  
  
    # 用非 贪婪模式 匹配 任意<p>标签  
    BgnPartRex = re.compile("<p.*?>")  
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")  
    CharToNextTabRex = re.compile("<td>")  
  
    # 将一些html的符号实体转变为原始符号  
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
#----------- 处理页面上的各种标签 -----------    
  
  
class MM_Spider:  
    # 构造函数  
    def __init__(self,url):  
        self.myUrl=url  
        self.urlNum=0  
        self.myTool = HTML_Tool()   
  
    #header伪装获得html内容  
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
  
  
    #每个线程去抓一个人的图，简介等，要自己组织文件目录  
    def working(self):  
        while True:  
            url=Q.get()  
            self.get_MM_pic(url)  
            #sleep(1)  
            Q.task_done()  
              
    def get_MM_pic(self,url):  
        personal_page=self.get_html(url)  
        #<title>少女時代 | 美女图集 —— 美女图片 美女写真</title>  
        title=re.search(r'<title>([^ |]*)',personal_page,re.S)  
        print title.group(1)  
        os.mkdir(title.group(1))  
        #<div class="column grid_12" style="margin-bottom: 10px">  
        #</div>  
        profile=re.search(r'<div class="column grid_12" style="margin-bottom: 10px">([^<]*)',personal_page,re.S)  
          
        f = open(title.group(1)+'/'+title.group(1)+'简介'+'.txt','w+')  
        if profile==None:  
            f.writelines("no profile")  
        else:  
            f.writelines(self.myTool.Replace_Char(profile.group(1)))  
        f.close()  
         #<div class="grid_title">  
        #<a href='http://girl-atlas.com/a/10140314061500000191' class="caption">[NS Eyes] #184 Sayaka Isoyama 磯山さやか</a>  
        #</div>  
        album=re.findall(r'<a href=\'([^\']*)\' class="caption">',personal_page,re.S)  
        count=0  
        for item in album:  
            print item  
            #raw_input()  
            count=self.save_MM_page(item,title.group(1),count)  
  
  
    def save_MM_page(self,url,catalog,count):  
        photos_page=self.get_html(url)  
        #<img title="2011 Girls Generation『Holiday』1st Part - No. 24 - 24" delay='http://girlatlas.b0.upaiyun.com/45/20121223/0041f70328b00e5535e2.jpg!mid' />  
        photos=re.findall(r"<img title=.*?delay='(.*?)' />",photos_page,re.S)  
        for item in photos:  
            urllib.urlretrieve(item,catalog+ '/'+'%d.jpg' %count)  
            #print catalog  
            count+=1  
        return count  
              
              
    #主函数  
    def MM_pic(self):  
        #设置编码
        reload(sys)  
        sys.setdefaultencoding('utf8')  
        #切换目录  
        os.chdir('pics')  
        #准备线程池  
        for i in range(thread_num):  
            t=Thread(target=self.working)  
            t.setDaemon(True)  
            t.start()  
        #往队列中放入任务  
        myPage=self.get_html(self.myUrl).encode('GB18030')
        #<li title='矶山さやか' tid='10' length='13'><a target="_blank" href="http://girl-atlas.com/t/10">矶山さやか</a></li>  
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
