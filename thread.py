#!/usr/bin/env python
#encoding:UTF-8
 
import re
import urllib  
import threading
import time
import Queue
 
 
def getHtml(url):
    html_page=urllib.urlopen(url).read()
    return html_page
 
 
#��ȡ��ҳ��ͼƬ��URL
def getUrl(html):
    pattern=r'http://.*?\.jpg!mid'   #������ʽ  .*?(ƥ��http://��\.jpg!mid֮�������ַ���)
    imgre=re.compile(pattern)
    imglist=re.findall(imgre,html)   #re.findall(pattern,string)  ��string��Ѱ������ƥ��ɹ����ַ��������б���ʽ����ֵ
    return imglist
 
 
class getImg(threading.Thread):
    def __init__(self,queue):        #���̼�ͨ������ͨ�ţ�����ÿ��������Ҫ�õ�ͬһ�����г�ʼ��
        threading.Thread.__init__(self)
        self.queue=queue
        #self.setDaemon(True)         #�ػ��߳�
        self.start()                 #�����߳�
     
    #ʹ�ö���ʵ�ֽ��̼�ͨ��
    def run(self):
        global count
        while (True):
            imgurl = self.queue.get()
            print self.getName()
 
            #urllib.urlretrieve(url,filname) ��url��������ȡ������������filename��
            urllib.urlretrieve(imgurl, 'F:/mm/1.jpg')
        #   print "%s.jpg done"%count
            count += 1
            if self.queue.empty():
                break
            self.queue.task_done()  #��ʹ�����̵߳��� task_done() �Ա�ʾ�����˸���Ŀ������������еĹ���ʱ����ôδ��ɵ�����������ͻ���١�
 
 
 
def main():
    global count
    url="http://girl-atlas.com/a/10130205170100000231"  #Ҫ������ҳ��ַ
    html=getHtml(url)
    imglist=getUrl(html)
    threads=[]
    count=0
    queue=Queue.Queue()
 
    #����������������
    for i in range(len(imglist)):
        queue.put(imglist[i])
     
    #���߳���ȥͼƬ
    print 'aaa'
    for i in range(4):
        thread=getImg(queue)
        threads.append(thread)
     
    #�ϲ����̣����ӽ��̽���ʱ�������̲ſ���ִ��
    #for thread in threads:
    #   thread.join()
 
    #��һ�ֱ��������������ķ������η�����ǰ���self.queue.task_tone()����Ӧ
    #����Ҫͬʱʹ��
    #queue.join()
 
 
if __name__=='__main__':
    main()
    print "Down"
