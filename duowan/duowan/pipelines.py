#-*- coding: utf-8 -*-  
#coding��UTF-8  
import urllib  
import urllib2  
import time  
import os    
import shutil  
from scrapy.exceptions import DropItem  
import pymongo  
  
#Pineline���ڴ����ȡ����item����  
class GifPipeline(object):  
  
    #��������ʱִ�У��½�һ����Ϊgaoxiao_gif���ļ�  
    #����һ����Ϊgif_url��mongo���ݿ�, ������һ������my_collection  
    #����һ����Ϊgif_url��txt�ļ�  
    def __init__(self):  
        #conn = pymongo.MongoClient('localhost', 27017)  
        #db = conn['gif_url']  
        #self.collection = db['gif_collection']  
  
        self.f = open('url_gif.txt', 'wb')  
          
        if os.path.exists('gaoxiao_gif'):    
            shutil.rmtree("gaoxiao_gif")    
        else:    
            os.mkdir("gaoxiao_gif")  
  
  
    #��������ʱ���ã������ȡ����item����,ע��item��ÿһ��ҳ������ݼ���  
    def process_item(self, item, spider):  
        #ȥ��û�õ�����  
        if item['gif_url']:  
              
            #����ÿ��ҳ��item�������������url  
            #�ַ����жϣ���������.jpg��.png�ļ���ֻ����gif�ļ�  
            #��url����mongo���ݿ�  
            #��url��Ž�txt���Ժ������Ѹ������  
            for i in item['gif_url']:  
                if ".gif" in i:  
                    self.f.write(i)  
                    self.f.write('\r\n')  
  
                    #gif_url=[{"url":i}]  
                    #self.collection.insert(gif_url)  
                  
                    now = time.localtime(time.time())  
                    fname = str(now)  
                    urllib.urlretrieve(i, 'gaoxiao_gif/%s.gif' %fname)  
        else:  
            raise DropItem(item)  
        return item  
  
  
    #����ر�ʱ����  
    def close_spider(self, spider):  
        print("Done")  
