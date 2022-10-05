# -*- coding:utf-8 -*-

import scrapy
import os,time
import json
from bs4 import BeautifulSoup

import math
import numpy as np
import pickle
import codecs


UspApiPatch = r"C:\Users\jalen\PycharmProjects\pythonProject\ecspider\Data"


# 常見的file操作模式：
# read打開&讀取
# – r：打開指定文件，只用於reading。文件的指針在開頭。python的默認模式。若無指定文件則報錯
# –· rb：以二進制執行的r；
#
# write打開&覆蓋
# – w：打開指定文件，只用於writing。如果文件存在，則先刪除（表裡所有的）已有數據，如果不存在，則創建；
# – wb：以二進制執行的w；
#
# append打開&添加
# – a：打開指定文件，用於appending。如果文件存在，指針放在結尾，如果文件不存在，則創建；
# – ab：以二進制執行的a；
# Python 的 pickle 模組的 dump() 函式。
# NumPy 庫的 save() 函式。
# Python json 模組的 dump() 函式。
def getcategoryTemp(cate_source):
        cate_dict = []  # 累加 dict
        try:
            #cate_source = getResponseContent('https://online.skm.com.tw/', "","https://online.skm.com.tw/", useragent)
            print('取目錄中請稍後...休息1秒...')
            time.sleep(1)  ## delays for 1 seconds
            cate_soup = BeautifulSoup(cate_source, 'lxml')
            #https://online.skm.com.tw/product_category/1_180
            for menu_div in cate_soup.find_all('div',attrs={'class':'offcanvas-menu'}):
                try:
                    for menu_li_1 in menu_div.find_all('li'):
                        try:
                            for menu_li_1_a in menu_li_1.find_all('a', attrs={'data-level': '1'}):
                                c_link = "https://online.skm.com.tw/product_category/1_" + str(menu_li_1_a['data-id'])
                                c_name = menu_li_1_a.text
                                c_name = c_name
                                os.system("cls")  # 清除畫面
                                try:
                                    print('取得目錄 %s-商品頁' % str(c_name))
                                except Exception as ex:
                                    print('取得目錄 %s-商品頁' % str(c_link))
                                if c_link!="" and c_name!="":
                                    df_products = dict()
                                    df_products.setdefault('CategoryURL', c_link)
                                    df_products.setdefault('CategoryName', c_name)
                                    cate_dict.append(df_products)

                        except Exception as ex:
                            pass
                except Exception as ex:
                    pass

            if len(cate_dict)>0:
               #存成.pkl檔
               # with open(UspApiPatch + '\\' + "category.pkl", "wb") as tf:
               #    pickle.dump(cate_dict, tf)

               #存成.numpy檔
               #np.save(UspApiPatch + '\\' + 'category', cate_dict)
               #存成.josn檔
               tf = open(UspApiPatch + '\\' + "category.json", "w")
               json.dump(cate_dict, tf)
               tf.close()
               # # 將字典資料存入txt檔案
               # f = codecs.open(UspApiPatch + '\\' + "category.txt", 'w',"utf-8")  # 以'w'方式開啟檔案
               # for p_dict in range(len(cate_dict)):
               #     s1 = str(cate_dict[p_dict]['CategoryURL'])  # 把字典的值轉換成字元型
               #     s2 = str(cate_dict[p_dict]['CategoryName'])  # 把字典的值轉換成字元型
               #     f.write(s1 + ',' + s2 + '\n')  # 一行一個鍵值對
               # f.close()  # 關閉檔案
        except:
            pass


class proxySpider(scrapy.Spider):
    name = 'skm_example'
    allowed_domains = ['online.skm.com']
    start_urls = ['https://online.skm.com.tw/']

    def parse(self, response):
        getcategoryTemp(response.text)


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

        



