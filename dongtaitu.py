# -*- coding:utf-8 -*-
import urllib  
import urllib2  
import re  
import os  
import sys
import time
import socket
reload(sys)
sys.setdefaultencoding('utf-8')

#socket.setdefaulttimeout(20)

  
class Spider:  
    def __init__(self):  
        self.siteUrl="http://www.cecepa.com"  
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'  
        self.headers = { 'User-Agent' : self.user_agent }  
  
    def getPage(self,url):  
        url = self.siteUrl+url
        request = urllib2.Request(url,headers = self.headers)  
        try:
            response = urllib2.urlopen(request)  
            content = response.read()
            response.close()
            return content
        except Exception as e:
            return None
  
    def getIndex(self,pageIndex):  
        page = self.getPage(pageIndex)  
        if page is None:
            return
        #pattern = re.compile(r'<a.*?class="img_wrap".*?title="(.*?)"href="(.*?)".*?target="_blank".*?>',re.S|re.I)     # 这个正则不行，而且速度超级慢
        pattern = re.compile(r'<a class="img_wrap" title="(.*?)" href="(.*?)" target="_blank">',re.S|re.I) 
        items = re.findall(pattern,page)  
  
        contents=[]  
        for item in items:
            #if "动漫或同人CG".decode('gbk').encode("utf-8") in item[0]:
            if "CG" in item[0]:
                contents.append([item[0],item[1]])  
        return contents  
  
    def mk_dir(self,path):  
        isExisist = os.path.exists(path)  
        if not isExisist:  
            os.makedirs(path)  
            return True  
        else:
            return False  

    def getContent(self,url,dirname):
        count = 0
        for i in range(1,20):
            requestUrl = url + "index" + str(i) + ".html"
            page = self.getPage(requestUrl)
            if page is None:
                break;
            else:
                pattern = re.compile(r'<img width="990" src="(.*?)"',re.S|re.I) 
                items = re.findall(pattern,page)
                for item in items:
                    count = count + 1
                    self.downImage(item,dirname,count)  
                    time.sleep(1)
  
    def downImage(self,url,dirname,count):  
        imageUrl = url  
        request = urllib2.Request(imageUrl,headers = self.headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.reason
            return
        imageContents = response.read()
        response.close()
  
        urlArr = imageUrl.split(u".")  
        imageType = str(urlArr[len(urlArr)-1])  
  
        path = "F:/test/"+dirname.decode('utf8')  
  
        self.mk_dir(path)
        imagePath = path+u"/"+str(count)+u"."+imageType
        print imagePath

        f = open(imagePath, 'wb')  
        f.write(imageContents)  
        f.close()
  
    def downLoadAllPicture(self,PageIndex):  
        url = "/artkt/index"+str(PageIndex)+".html"  
        contents = self.getIndex(url)  
  
        for list in contents:  
            dirname  = list[0]  
            imageUrl = list[1]  
            self.getContent(imageUrl,dirname)

demo = Spider()  
print "start"
for page in range(20,30):  
    demo.downLoadAllPicture(page)  
print "end"
