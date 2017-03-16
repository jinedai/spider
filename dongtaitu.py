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

#socket.setdefaulttimeout(120)

class Spider:  
    def __init__(self, rooturl, filterstr):  
        self.siteUrl=rooturl
        self.filterStr =filterstr
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'  
        self.headers = { 'User-Agent' : self.user_agent }  

    def getPage(self,url):  
        url = self.siteUrl+url
        request = urllib2.Request(url,headers = self.headers)  
        try:
            response = urllib2.urlopen(request,None,20)  
            content = response.read()
            response.close()
            return content
        except urllib2.URLError, e:
            return None
        except socket.timeout, e:
            return None

    def getIndex(self,pageIndex):  
        page = self.getPage(pageIndex)  
        if page is None:
            return
        pattern = re.compile(r'<a class="img_wrap" title="(.*?)" href="(.*?)" target="_blank">',re.S|re.I) 
        items = re.findall(pattern,page)  

        contents=[]  
        for item in items:
            if not self.filterStr is None:
                if self.filterStr.decode('gbk').encode("utf-8") in item[0]:
                    contents.append([item[0],item[1]])  
                else:
                    continue
            else:
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
                    time.sleep(10)
        print dirname.decode("utf-8")+"  下载完成".decode("gbk").encode("utf-8")

    def downImage(self,url,dirname,count):  
        imageUrl = url  
        request = urllib2.Request(imageUrl,headers = self.headers)
        try:
            response = urllib2.urlopen(request,None,20)
            imageContents = response.read()
            response.close()
        except urllib2.URLError, e:
            print e.reason
            return
        except socket.timeout, e:
            print url+u"socket time out"
            return

        urlArr = imageUrl.split(u".")  
        imageType = str(urlArr[len(urlArr)-1])  

        path = "F:/test/"+dirname.decode('utf-8')  

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

rooturl     = "http://www.cecepa.com"  
filterstr   = "高质量CG"
demo = Spider(rooturl,filterstr)  
print "start"
for page in range(1,150):  
    print page
    demo.downLoadAllPicture(page)  
print "end"
