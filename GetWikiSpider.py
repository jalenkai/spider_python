import urllib3
import pymssql
import time
import os
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from spiderscomm.customUserAgent import  RandomUserAgent  as UAT
from goto import with_goto

from spiderscomm.langconv import *
from wikiapi import WikiApi

import command as comm
import threading
from difflib import SequenceMatcher as SM


class GetWikiSpider(object):
      def __init__(self,key_name):
          self.key_name = key_name
          self.url =""
          self.wiki_content=""
          self.img=""
          self.wiki_heading=""
          self.getWiki(key_name)


      def getWiki(self,entity):
          print("取得HTML資料!!")
          self.wiki_content  = ""
          self.url = str("https://zh.wikipedia.org/zh-tw/") + urllib.parse.quote(entity)
          self.img = ""
          self.wiki_heading = ""
          wiki_img =""
          wiki_word_content =""

          #driver.get(self.url)
          #htmlContent = driver.page_source
          htmlContent = getResponseContent(self.url,_cookies,_useragent)
          #休息...............................
          time.sleep(2) #delays for 2 seconds
          wiki_soup = BeautifulSoup(htmlContent,'lxml') 
          #<meta property="og:image"
          try:
             wiki_img = ""
             img_meta= wiki_soup.find_all(name='meta')
             for items_meta in img_meta:
                 try:
                    #property="og:image"
                    if (str(items_meta).find(str('og:image')) > -1) :
                        wiki_img = comm.StartEndStrTrun(str(items_meta),'content="','property="')
                        wiki_img = wiki_img.replace('"','').lstrip().rstrip()
                        break
                 except:
                    pass
          except:
              img_meta = ""

          itemText = wiki_soup.find(name='div', id='mw-content-text')
          #只爬第一個標題 文章敘述
          try:
              print("spider圖片")
              if (wiki_img==""):
                 thumb_content = itemText.find_all('div', attrs={'class':'thumb tright'})[0]
                 img_htmlcods = thumb_content.find_all('div', attrs={'class':'thumbinner'})[0]
                 wrapper_a = img_htmlcods.a
                 wiki_img = "https:" + wrapper_a.find('img')['src']
          except: 
              print("無圖片")
              wiki_img =""
              
          item_word_s =0
          wiki_word_content =""
          print("取得wiki資料!!")
          itcs = itemText.contents[0]
          for items_c in itcs.contents:
              content_p = items_c.name
              if (content_p == "h2"):
                 break;
              #檢視cods
              if (content_p == "p"):
                 item_word_s += 1
                 #if (item_word_s >3):#只匯入有3段 文章
                 #   break;
                 wiki_htmlcods = comm.filter_tags(items_c.text)
                 if (item_word_s==1):
                    wiki_word_content = str(wiki_htmlcods.rstrip())
                    break;
                 else:
                    if (wiki_htmlcods!=""):
                       wiki_word_content +=  str("<p>") + str(wiki_htmlcods.rstrip()) 
                       break;
                    else: 
                       wiki_word_content = str(wiki_htmlcods.rstrip())
                       break;

          #into
          self.wiki_content = ""
          self.img = ""
          if (wiki_word_content!=""):
             if  (len(wiki_word_content)>20) :
                wiki_word_content = re.sub("["+ r"[1-9]" + "]","",wiki_word_content).replace("[","")
                #if (wiki_word_content.find(comm.simple2tradition(entity))>0):
                self.wiki_content = wiki_word_content.replace("<p>","")
                self.img  = wiki_img
          else:
             try :
                #方法2.呼叫api會有調用次數限制20200424
                results = wiki.find(comm.simple2tradition(entity))
                #print (results)
                ##取出相符合的資料list
                for article_c in results:
                   article = wiki.get_article(article_c)
          #    #article.heading 與 self.key_name 比對相似度;取出最合適 維基百科 summary
                   token_s = 0
                   token = 0 
                   if (article.summary.find(entity)>0):
                      token_s = token_s + 0.2

                   if (token_s>0):#內容上並無 key_name關鍵字故無需收錄
                      token = SM(None, article.heading, comm.simple2tradition(self.key_name)).ratio()
                      if (len(self.key_name)<len(article.heading)):
                         if (token<=0.8):
                            continue

                      token += token_s 
                      if (token<=0.7):
                         continue

                      spilt_s =0
                      spilt_e =0
                      self.wiki_content  = ""
                      self.url = ""
                      self.img = ""
                      self.wiki_heading = ""
                      wiki_content = ""
                      if (article.summary.find('。\n')>0):
                         spilt_e = article.summary.find('。\n') + 1
                         wiki_content = comm.filter_tags(article.summary[0:spilt_e])
                      else :
                         spilt_e = article.summary.find('。')
                         wiki_content = comm.filter_tags(article.summary[0:spilt_e])

                      if (wiki_content!=""):
                         self.wiki_content = comm.simple2tradition(comm.filter_tags(wiki_content))

                      self.url = article.url
                      try : #http:None
                          if (article.image!='' and article.image!='http:None'):
                             self.img = str(article.image).replace('http:','https:')
                          else :
                             self.img= ''
                      except:
                         self.img= ''

                      self.wiki_heading = comm.simple2tradition(comm.filter_tags(article.heading))
                      print ("取得wiki資料")

                      if (token>=1 or token>=0.65 ):
                        break
             except:
                 pass
              
if __name__ == '__main__':
   chrome_options = webdriver.ChromeOptions()
   chrome_path = "C:\selenium_driver\chromedriver.exe"
   #添加UA
   #chrome_options.add_argument('user-agent="' + _useragent + '"')
   chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
   chrome_options.add_argument('--no-sandbox') #以最高权限运行
   chrome_options.add_argument('--disable-dev-shm-usage') #足够的资源分配给Docker容器
   chrome_options.add_argument("--disable-notifications")
   ###禁用浏览器弹窗
   prefs = {  
    'profile.default_content_setting_values' :  {  
        'notifications' : 2  
     }  
   }  
   chrome_options.add_experimental_option('prefs',prefs)
   chrome_options.add_argument('--headless')#無介面模式 
   driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
   driver.maximize_window()
   driver.implicitly_wait(30) # seconds
   driver.get('https://zh.wikipedia.org/wiki/Wiki')
   time.sleep(3) ## delays for 3 seconds

   _cookies = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()])
   _useragent = UAT.process_request(__name__)
    
    GetWikiSpider('國際牌')
    
