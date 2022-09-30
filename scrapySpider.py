# -*- coding:utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
#from selenium import webdriver
import os

class proxySpider(scrapy.Spider):
    #爬蟲名字
    name = 'proxy_example'
    #允許訪問的網域名稱
    allowed_domains = ['www.us-proxy.org']
    #起始的url，指的是第一次訪問的url
    start_urls = ['http://www.us-proxy.org']
    #執行start_urls 的調回方法，方法中的response 就是返回的對象
    #相當於response = urllib.request.urlopen(urls)
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        os.system("cls") #清除畫面
        trs = soup.find_all("table" , class_ ='table table-striped table-bordered')
        for tr in trs:
            tds = tr.select("td")
            if len(tds) > 6:
                print(tds)

    # def parse_item(self, response):
        #這裡的item 是用一個dict 字典存取數據
        # item = {}
        # div_list = response.xpath('//div[@class="bookslist"]/ul/li/div')
        # for div in div_list:
            #data-original 表示圖片是載入，不能擷取src属性
            # src = div.xpath('./div/a/img/@data-original').extract_first()
            # name = div.xpath('./div/a/img/@alt').extract_first()
            # author = div.xpath('./p[1]/a[1]/text()|./p[1]/text()').extract_first()
            # url = div.xpath('./div/a/@href').extract_first()
            # url = "https://www.dushu.com" + url
            # yield scrapy.Request(url=url, callback=self.parse_second, meta={'name': name, 'src': src, 'author': author})

    # def parse_second(self, response):
        # price = response.xpath('//div[@class="book-details"]//span/text()').get()
        # name = response.meta['name']
        # src = response.meta['src']
        # author = response.meta['author']
        # yield DushuItem(src=src, name=name, author=author, price=price)

# if __name__ == '__main__':
#     chrome_options = webdriver.ChromeOptions()
#     chrome_path = "C:\selenium_driver\chromedriver.exe"
#     # chrome_options.add_argument('--headless')#無介面模式
#     driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
#     driver.implicitly_wait(50)  # seconds
#     driver.get('http://www.us-proxy.org')
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'lxml')
#     trs = soup.find_all("table" , attrs={'class': 'table table-striped table-bordered'})
#     for tr in trs:
#         tds = tr.select("td")
#         if len(tds) > 6:
#             print(tds)

        



