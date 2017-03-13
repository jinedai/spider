__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
 
#���°ٿ�������
class QSBK:
 
    #��ʼ������������һЩ����
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #��ʼ��headers
        self.headers = { 'User-Agent' : self.user_agent }
        #��Ŷ��ӵı�����ÿһ��Ԫ����ÿһҳ�Ķ�����
        self.stories = []
        #��ų����Ƿ�������еı���
        self.enable = False
    #����ĳһҳ���������ҳ�����
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #���������request
            request = urllib2.Request(url,headers = self.headers)
            #����urlopen��ȡҳ�����
            response = urllib2.urlopen(request)
            #��ҳ��ת��ΪUTF-8����
            pageCode = response.read().decode('utf-8')
            return pageCode
 
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"�������°ٿ�ʧ��,����ԭ��",e.reason
                return None
 
    #����ĳһҳ���룬���ر�ҳ����ͼƬ�Ķ����б�
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "ҳ�����ʧ��...."
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class'+
                         '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #�����洢ÿҳ�Ķ�����
        pageStories = []
        #�����������ʽƥ�����Ϣ
        for item in items:
            #�Ƿ���ͼƬ
            haveImg = re.search("img",item[3])
            #���������ͼƬ����������list��
            if not haveImg:
                #item[0]��һ�����ӵķ����ߣ�item[1]�Ƿ���ʱ��,item[2]�����ݣ�item[4]�ǵ�����
                pageStories.append([item[0].strip(),item[1].strip(),item[2].strip(),item[4].strip()])
        return pageStories
 
    #���ز���ȡҳ������ݣ����뵽�б���
    def loadPage(self):
        #�����ǰδ����ҳ������2ҳ���������һҳ
        if self.enable == True:
            if len(self.stories) < 2:
                #��ȡ��һҳ
                pageStories = self.getPageItems(self.pageIndex)
                #����ҳ�Ķ��Ӵ�ŵ�ȫ��list��
                if pageStories:
                    self.stories.append(pageStories)
                    #��ȡ��֮��ҳ��������һ����ʾ�´ζ�ȡ��һҳ
                    self.pageIndex += 1
 
    #���ø÷�����ÿ���ûس���ӡ���һ������
    def getOneStory(self,pageStories,page):
        #����һҳ�Ķ���
        for story in pageStories:
            #�ȴ��û�����
            input = raw_input()
            #ÿ������س�һ�Σ��ж�һ���Ƿ�Ҫ������ҳ��
            self.loadPage()
            #�������Q��������
            if input == "Q":
                self.enable = False
                return
            print u"��%dҳ\t������:%s\t����ʱ��:%s\n%s\n��:%s\n" %(page,story[0],story[1],story[2],story[3])
 
    #��ʼ����
    def start(self):
        print u"���ڶ�ȡ���°ٿ�,���س��鿴�¶��ӣ�Q�˳�"
        #ʹ����ΪTrue�����������������
        self.enable = True
        #�ȼ���һҳ����
        self.loadPage()
        #�ֲ����������Ƶ�ǰ�����˵ڼ�ҳ
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #��ȫ��list�л�ȡһҳ�Ķ���
                pageStories = self.stories[0]
                #��ǰ������ҳ����һ
                nowPage += 1
                #��ȫ��list�е�һ��Ԫ��ɾ������Ϊ�Ѿ�ȡ��
                del self.stories[0]
                #�����ҳ�Ķ���
                self.getOneStory(pageStories,nowPage)
 
spider = QSBK()
spider.start()