#-*- coding: utf-8 -*-  
#coding��UTF-8  
from scrapy.spiders import CrawlSpider, Rule  
from scrapy.linkextractors.sgml import SgmlLinkExtractor  
from duowan.items import GifItem  
  
  
class GifSpider(CrawlSpider):  
  
    #�������֣�Ψһ�����������Ժ��½�������  
    name = "gif"  
  
    #��ѡ��������ȡ���򣬳�����������Ӳ���ȡ  
    allowed_domains = ["duowan.com"]  
      
    #���忪ʼ��ȡ��ҳ��A  
    start_urls=["http://tu.duowan.com/scroll/100103.html"]  
      
    #���������ҳ��A����ȡ���Ϲ�������ӣ������ú�������  
    rules = [  
        Rule(SgmlLinkExtractor(allow=('/scroll/\d*/\d*.html')),  callback = 'parse_gif', follow=True),  
        Rule(SgmlLinkExtractor(allow=('/scroll/\d*.html')),  callback = 'parse_gif', follow=True),  
        ]  
  
    def parse_gif(self, response):  
        #�����ȡ���ݵĽṹ  
        urlItem = GifItem()  
          
        #ע��item��ÿ��ҳ������ݼ���,ÿ��ҳ����һ��item���Ѽ�����ý���Pipeline����  
        urlItem['gif_url'] = response.selector.xpath('//*[@id="picture-pageshow"]/div[1]/div[@class="pic-box"]/a/img/@src').extract()  
        yield urlItem  
