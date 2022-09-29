# -*- coding:utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
#from selenium import webdriver


class proxySpider(scrapy.Spider):
    name = 'proxy_example'
    allowed_domains = ['www.us-proxy.org']
    start_urls = ['http://www.us-proxy.org']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        trs = soup.find_all("table" , class_ ='table table-striped table-bordered')
        for tr in trs:
            tds = tr.select("td")
            if len(tds) > 6:
                print(tds)


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

        



