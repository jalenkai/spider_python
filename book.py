# -*- coding:utf-8 -*-
#import sys 頁面連結錯誤

import spiderscomm
import urllib3
import pymssql
import time
import cursor
import time
import os,hashlib

from spiderscomm.langconv import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from spiderscomm.customUserAgent import  RandomUserAgent  as UAT
from os import getenv
#from goto import with_goto
from lxml import etree 
from multiprocessing import Pool
import random
import command as comm
import threading
import requests

sqlserverIP = 'xxx.xxx.xxx.xxx'#sql位置ip
m_id="電商ID"
trackcode =str("https://adcenter.conn.tw/redirect_wa.php?k=f7c39f1a7e62bb984307e385e460604b&tourl=")

ipaddr = comm.get_ip_address()
UspApiPatch = "SQL位置檔案的路徑"
Dstfilename ="檔案產生的路徑"
cname=""
setPageCnt = 300
runtimeint = 7

class Item(object):
    # define the fields for your item here like:
    g_name = None   #商品名稱
    g_link = None   #商品連結
    g_Rprice = None #商品特價(實際fp上要揭露價格)
    g_Sprice = None #商品售價
    g_image = None  #商品圖片
    c_name = None   #商品目錄名稱

def getproxies2csvListSetHtmlContents(FileName,curl,headersItems):
   # 開啟 CSV 檔案
   response = ""
   ActIpsList = []
   with open(FileName, newline='') as csvfile:
       # 讀取 CSV 檔案內容
       rows = csv.reader(csvfile)
       # 以迴圈輸出每一列
       for row in rows:
         proxy = {'http':'http://'+ row[0] + ':' + row[1],
         'https':'https://'+ row[0]  + ':' + row[1]}
         try:
             resp = requests.get(curl, headers=headersItems,proxies=proxy, timeout=60)
             if str(resp.status_code) == '200': 
                 print('Succed: {}:{}'.format(row[0], row[1]))
                 response = resp
                 break;
             else:
                 print('Failed: {}:{}'.format(row[0], row[1]))
                 response = ""
         except:
               print('Failed: {}:{}'.format(row[0], row[1]))
               response = ""
   return response.text

class GetbooksSpider(object):
    
    def __init__(self, url,cateurl,cname,recno,_cookies,_useragent):
        _useragent = UAT.process_request(self)
        self.cookies = _cookies
        self.useragent = _useragent
        self.url = url
        self.cateurl = cateurl
        self.cname = cname
        PageTotalCount = self.spiderPageTotalCount(self.url)
        self.pageSum = int(PageTotalCount)  #必須要讀取url總頁數
        if (self.pageSum>0):
           self.urls = self.getUrls(self.pageSum)
           self.items =self.spider(self.urls,recno)
        else:
           time.sleep(120)
           PageTotalCount = self.spiderPageTotalCount(self.url)
           self.pageSum = int(PageTotalCount)  #必須要讀取url總頁數
           if (self.pageSum>0):
              self.urls = self.getUrls(self.pageSum)
              self.items =self.spider(self.urls,recno)
           else:
              print("無資料可讀取!!")

    def getUrls(self,pageSum):
        urls = []
        pagenum = [str((i*1)+1) for i in range(pageSum)]
        ul = self.url.split('&page=') #將連結=字串分解
        #先取得第一頁得到總頁數
        for page in pagenum:
            ul[-1] = page
            url = '&page='.join(ul) 
            urls.append(url)
        return urls
    
#傳入第一頁<div class="cnt_page">
    def spiderPageTotalCount(self,url):
            print("取得HTML資料!!") 
            try :
               htmlContent = self.getResponseContent(url)
            except :
                pass
                  #driver.implicitly_wait(5) # seconds
                  #driver.get(str(url))#傳入第一層目錄URL
                  #time.sleep(2) ## delays for 2 seconds
                  #htmlContent = driver.page_source #取得原始碼

            PageTotalCount = 0
            if (htmlContent!=""):
               soup = BeautifulSoup(htmlContent,'lxml')
               if (len(soup)>0):
                  Errorstr = soup.find(str('頁面連結錯誤'))
                  if (Errorstr=="" or Errorstr==None):              
                     for itemText_cname in soup.find_all('meta', attrs={'property':'og:title'}):
                         cname =itemText_cname['content'].replace('"','').replace(str('>'),str('＞')) #目錄名稱
                         self.cname = cname

                     #<div class="page">共<span>20</span>頁
                     for itemText in soup.find_all('div', attrs={'class':'page'}):
                         PageTotalCount = itemText.find('span').get_text().strip()
                     #有價格標籤才有商品資訊必要條件
                     try : #<span class="price">
                           if (PageTotalCount==0 and len(soup.find('span', attrs={'class':'price'})) > 0):        
                               PageTotalCount=1
                     except :
                        pass

                     try : #<ul class="price">
                        if (PageTotalCount==0 and len(soup.find('ul', attrs={'class':'price'})) > 0):        
                            PageTotalCount=1
                     except :
                        pass

                     if (int(PageTotalCount) > int(setPageCnt)) : #最大頁數
                         PageTotalCount = setPageCnt

            os.system("cls") #清除畫面
            return PageTotalCount
   
    def spider(self,urls,recno):
        items = []
        pagecnt = 0
        g_link = ''
        xmlfilechk = False
        #定義xml格式 cname =  self.cname
        _root = etree.Element("productList")  
        for url in urls:          
            pagecnt +=1
            #一般商品區
            if(url.find('/cd/') < 0 and url.find('/dvd/') < 0): 
                try :
                  htmlContent = self.getResponseContent(url)
                except :
                  pass
                  #driver.implicitly_wait(5) # seconds
                  #driver.get(str(url))#傳入第一層目錄URL
                  #time.sleep(5) ## delays for 2 seconds
                  #htmlContent = driver.page_source #取得原始碼

                if (htmlContent !=''):     
                   time.sleep(3) ## delays for 3 seconds
                   soup = BeautifulSoup(htmlContent,'lxml')
                   if (len(soup)>0):
                     for itemText in soup.find_all('ul', attrs={'class':'cntli_001 cntli_001a clearfix'}):
                       cntint=0
                       items = Item()
                       for wrapperlist in itemText.find_all('li'):  
                           try:     
                               g_link = wrapperlist.find('a')['href']
                               items.g_link = str(trackcode) + g_link.replace("://","%3A%2F%2F").replace(str("/"),"%2F").replace(str('?'),'%3F').replace(str('&'),'%26').replace(str('='),'%3D')
                           except: 
                                 #會有 <li class="hr_a"></li> 的標籤
                                 items.g_link =""
                                 print("class='hr_a';例外跳離!!")
                                 continue
                              
                           if (items.g_link!=""):
                              cntint +=1
                              os.system("cls") #清除畫面
                              print('目前抓取目錄:%s' % (str(self.cateurl))) 
                              print('共%d頁，目前正在抓取第 %d 頁資料第 %d 筆' % (int(self.pageSum),int(pagecnt),int(cntint))) 
                              try:
                                 items.g_image = wrapperlist.find('img')['src']
                              except:
                                  continue

                              if (items.g_image!='' and  items.g_image.find('http://') ==0):
                                  items.g_image = str(items.g_image).replace("http://","https://")
                              elif (items.g_image!='' and  items.g_image.find('https://')==0 ):
                                  items.g_image = str(items.g_image)
                              elif(items.g_image!='' and  (items.g_image.find('//')==0) ):
                                  items.g_image = str('https:') + str(items.g_image) 
                              elif(items.g_image!='' and  (items.g_image.find('://')==0) ):
                                  items.g_image = str('https') + str(items.g_image) 
                              elif (items.g_image.find('images/no-product') >-1) :
                                  items.g_image =''
                              else:
                                  items.g_image =''

                              try :
                                  for g_nameContent in wrapperlist.find('h4'):
                                      items.g_name = comm.filter_tags(g_nameContent.contents[0].replace("'",""))
                              except: 
                                 items.g_name  = ""
                                 continue

                              try :
                                  for priceContent in wrapperlist.find_all('span', attrs={'class':'price'}):
                                      items.g_Rprice = str(priceContent.find('strong').b.contents[0].replace("'",""))
                              except:
                                 items.g_Rprice = 0
                                 continue

                              if ( items.g_name !='' and items.g_Rprice!=0 and   items.g_image !='' and items.g_name.find('勿下標')<0 and  items.g_name.find('缺貨')<0 and items.g_name.find('備貨')<0 and items.g_name.find('補貨')<0 and items.g_name.find('售完')<0 and items.g_name.find('代購')<0 and items.g_name.find('退貨專區')<0  and items.g_name.find('專用賣場')<0 ):
                                 try :
                                    _body = etree.SubElement(_root,"Products")   
                                    etree.SubElement(_body, "ProductName").text = etree.CDATA(str(items.g_name.strip())) 
                                    etree.SubElement(_body, "BuyURL").text = etree.CDATA(str(items.g_link).strip())
                                    etree.SubElement(_body, "ProductImage").text = etree.CDATA(str(items.g_image.strip()))
                                    etree.SubElement(_body, "SalePrice").text = etree.CDATA(str(items.g_Rprice).replace(",","").strip())
                                    etree.SubElement(_body, "CategoryURL").text = etree.CDATA(str(str(self.cateurl).strip()))
                                    etree.SubElement(_body, "CategoryName").text = etree.CDATA(str(self.cname.replace("'","")).strip())
                                    xmlfilechk = True
                                 except: 
                                       print ("items[]存取錯誤!!")
                 
                        
                    
                       #for wrapperlist in itemText.find_all('li'):......
                     #for itemText in ContentText:......
             #if(url.find('/cd/') < 0 and url.find('/dvd/') < 0 ): ......
            elif(url.find('/cd/') >-1 or url.find('/dvd/') >-1 ):   #cd and dvd 影音專區  
                  if (url.find('https://www.books.com.tw/web/sys_avbotm/cd/0408/?loc=P_0002_2_008') >-1) and pagecnt>=100:
                      xmlfilechk==True
                      break
                  try :
                    htmlContent = self.getResponseContent(url)
                  except :
                     driver.implicitly_wait(5) # seconds
                     driver.get(str(url))#傳入第一層目錄URL
                     time.sleep(5) ## delays for 5 seconds
                     htmlContent = driver.page_source #取得原始碼

                  if (htmlContent !=''):
                     time.sleep(5) 
                     soup = BeautifulSoup(htmlContent,'lxml')
                     if (len(soup.find_all('div', attrs={'class':'item'}))>0):
                       for itemText in soup.find_all('div', attrs={'class':'wrap'}):
                         cntint=0
                         items = Item()
                      # 除了有class= item  也有  class= item last 的商品 
                      # For 第一種 class= item 
                      #for wrapperlist in itemText.find_all('div', attrs={'class':'item'}): ......
                         for wrapperlist in itemText.find_all('div', attrs={'class':'item'}):

                             try:
                                g_link = wrapperlist.find('a')['href']
                                items.g_link = str(trackcode) + g_link.replace("://","%3A%2F%2F").replace(str("/"),"%2F").replace(str('?'),'%3F').replace(str('&'),'%26').replace(str('='),'%3D').strip()
                             except: 
                                 #會有 <li class="hr_a"></li> 的標籤
                                 items.g_link =""
                                 continue

                             if (items.g_link!=""):
                                try:
                                    items.g_image = wrapperlist.find('img')['src']
                                except :
                                    continue

                                cntint +=1
                                os.system("cls") #清除畫面 
                                print('目前抓取目錄:%s' % (str(self.cateurl))) 
                                print('共%d頁，目前正在抓取第 %d 頁資料第 %d 筆' % (int(self.pageSum),int(pagecnt),int(cntint))) 
                                if (items.g_image!='' and  items.g_image.find('http://') ==0):
                                    items.g_image = str(items.g_image).replace("http://","https://")
                                elif (items.g_image!='' and  items.g_image.find('https://')==0 ):
                                  items.g_image = str(items.g_image)
                                elif(items.g_image!='' and  (items.g_image.find('//')==0) ):
                                 items.g_image = str('https:') + str(items.g_image) 
                                elif(items.g_image!='' and  (items.g_image.find('://')==0) ):
                                  items.g_image = str('https') + str(items.g_image) 
                                elif (items.g_image.find('images/no-product') >-1) :
                                  items.g_image =''
                                else:
                                  items.g_image =''

                                try :
                                    GPriceTextR=''
                                    GPriceTextS=''
                                    for g_nameContent in wrapperlist.find('h4'):
                                        items.g_name = g_nameContent.contents[0].replace("'","")

                                    for priceContent in wrapperlist.find_all('ul', attrs={'class':'price'}):
                                        #定價
                                        #優惠價
                                        GPriceTextR = priceContent.find_all('li', attrs={'class':'set2'})[0]
                                        GPriceTextR = GPriceTextR.find('strong').contents[0]
                                    if (str(GPriceTextS)!='') :  
                                        items.g_Rprice = str(GPriceTextS)
                                    if (str(GPriceTextR)!='') : 
                                        items.g_Rprice = str(GPriceTextR) 
                                except: 
                                      continue

                                if ( items.g_image !='' and items.g_name.find('勿下標')<0 and  items.g_name.find('缺貨')<0 and items.g_name.find('備貨')<0 and items.g_name.find('補貨')<0 and items.g_name.find('售完')<0 and items.g_name.find('代購')<0 and items.g_name.find('退貨專區')<0 and items.g_name.find('專用賣場')<0 ):
                                   try :
                                      _body = etree.SubElement(_root,"Products")   
                                      etree.SubElement(_body, "ProductName").text = etree.CDATA(str(items.g_name.strip())) 
                                      etree.SubElement(_body, "BuyURL").text = etree.CDATA(str(items.g_link).strip())
                                      etree.SubElement(_body, "ProductImage").text = etree.CDATA(str(items.g_image.strip()))
                                      etree.SubElement(_body, "SalePrice").text = etree.CDATA(str(items.g_Rprice).replace(",","").strip())
                                      etree.SubElement(_body, "CategoryURL").text = etree.CDATA(str(str(self.cateurl).strip()))
                                      etree.SubElement(_body, "CategoryName").text = etree.CDATA(str(self.cname.replace("'","")).strip())
                                      xmlfilechk = True
                                   except: 
                                        print ("items[]存取錯誤!!") 

                           #if (items.g_link!=""):......

                         # For 第二種 class= item last
                         for wrapperlist in itemText.find_all('div', attrs={'class':'item last'}):                                
                          try:
                             g_link = wrapperlist.find('a')['href']
                             items.g_link = str(trackcode) + g_link.replace("://","%3A%2F%2F").replace(str("/"),"%2F").replace(str('?'),'%3F').replace(str('&'),'%26').replace(str('='),'%3D').strip()
                          except: 
                              #會有 <li class="hr_a"></li> 的標籤
                              items.g_link =""
                              print("例外跳離!!")
                              continue

                          if (items.g_link!=""):
                             try :  
                                 items.g_image = wrapperlist.find('img')['src']
                             except :
                                 continue

                             cntint +=1
                             os.system("cls") #清除畫面
                             print('目前抓取目錄:%s' % (str(self.cateurl))) 
                             print('共%d頁，目前正在抓取第 %d 頁資料第 %d 筆' % (int(self.pageSum),int(pagecnt),int(cntint))) 
                             if (items.g_image!='' and  items.g_image.find('http://') ==0):
                                 items.g_image = str(items.g_image).replace("http://","https://")
                             elif (items.g_image!='' and  items.g_image.find('https://')==0 ):
                               items.g_image = str(items.g_image)
                             elif(items.g_image!='' and  (items.g_image.find('//')==0) ):
                              items.g_image = str('https:') + str(items.g_image) 
                             elif(items.g_image!='' and  (items.g_image.find('://')==0) ):
                               items.g_image = str('https') + str(items.g_image) 
                             elif (items.g_image.find('images/no-product') >-1) :
                               items.g_image =''
                             else:
                               items.g_image =''

                             try :
                                 GPriceTextR=''
                                 GPriceTextS=''
                                 for g_nameContent in wrapperlist.find('h4'):
                                     items.g_name = g_nameContent.contents[0].replace("'","")
                                 for priceContent in wrapperlist.find_all('ul', attrs={'class':'price'}):
                                     #定價                                  
                                    #優惠價
                                     GPriceTextR = priceContent.find_all('li', attrs={'class':'set2'})[0]
                                     GPriceTextR = GPriceTextR.find('strong').contents[0]
                                 if (str(GPriceTextS)!='') :  
                                     items.g_Rprice = str(GPriceTextS)
                                 if (str(GPriceTextR)!='') : 
                                     items.g_Rprice = str(GPriceTextR) 
                             except: 
                                   print ("g_nameContent存取錯誤!!")
                                   continue


                             if ( items.g_image !='' and items.g_name.find('勿下標')<0 and  items.g_name.find('缺貨')<0 and items.g_name.find('備貨')<0 and items.g_name.find('補貨')<0 and items.g_name.find('售完')<0 and items.g_name.find('代購')<0 and items.g_name.find('退貨專區')<0 and items.g_name.find('專用賣場')<0 ):
                                try :
                                   _body = etree.SubElement(_root,"Products")   
                                   etree.SubElement(_body, "ProductName").text = etree.CDATA(str(items.g_name.strip())) 
                                   etree.SubElement(_body, "BuyURL").text = etree.CDATA(str(items.g_link).strip())
                                   etree.SubElement(_body, "ProductImage").text = etree.CDATA(str(items.g_image.strip()))
                                   #etree.SubElement(_body, "ProductImage2").text = etree.CDATA(str("https://img.findprice.com.tw/ShowImg.ashx?m=") + str(items.g_image.replace("://","%3A%2F%2F").replace(str("/"),"%2F")  ).strip()) #   ,'?','%3D'),'&','%26')
                                   etree.SubElement(_body, "SalePrice").text = etree.CDATA(str(items.g_Rprice).replace(",","").strip())
                                   etree.SubElement(_body, "CategoryURL").text = etree.CDATA(str(str(self.cateurl).strip()))
                                   etree.SubElement(_body, "CategoryName").text = etree.CDATA(str(self.cname.replace("'","")).strip())
                                   xmlfilechk = True
                                except: 
                                     print ("items[]存取錯誤!!")

                          #if (items.g_link!=""):......                                
                        #for wrapperlist in itemText.find_all('div', attrs={'class':'item'}): ......
                  #for itemText in ContentText: ......
            #elif(url.find('/cd/') >-1 or url.find('/dvd/') >-1 ):......

        #2.存成xml或json檔案
        if (len(_root)>0):
           self.items =len(_root)  
           #2.存成xml檔案
           #檢查是否有此目錄
           if not os.path.isdir(str(Dstfilename)):  
              os.makedirs(Dstfilename )

           try:
              tree = etree.ElementTree(_root)
              filename = str(Dstfilename + r'\books' + str(recno) + '.xml')
              tree.write(filename, encoding="utf-8", xml_declaration=True)
           except:
               pass
           #直接存入SQL;先產生xml檔案;再由Net Form排成呼叫 是否 db_category.doflag全為0後在爬取店家資料
           #直接存入SQL
           if (os.path.exists(filename)):
              try:
                 filenameR = str(UspApiPatch + r'\books' + str(recno) + '.xml')    
                 execSQL = "EXEC SetXmlFile2PrimallTemp '" + str(m_id)  + "','" + filenameR + "'"
                 comm.CommitTable_dbname(execSQL,sqlserverIP,"apitemptb")  
                 os.rename(filename,filename + ".ok")
              except:
                 time.sleep(2) ## delays for 2 seconds
                 try:
                     filenameR = str(r'C:\XXXX\Data\books\books' + str(recno) + '.xml')    
                     execSQL = "EXEC SetXmlFile2PrimallTemp '" + str(m_id)  + "','" + filenameR + "'"
                     comm.CommitTable_dbname(execSQL,sqlserverIP,"apitemptb")  
                     os.rename(filename,filename + ".ok")
                 except:
                     os.rename(filename,filename + ".error") 

    def getResponseContent(self,url):
        try:
           headersItems = {
                            'Content-Type' : 'text/html;charset=UTF-8',
                            'Referer' : url,
                            'Upgrade-Insecure-Requests' : '1',
                            'Cookie': self.cookies,
                            'user-agent':  self.useragent 
           }    
           response =""  
           time.sleep(5)      
           resp = requests.get(url, headers=headersItems, timeout=120)
           if str(resp.status_code) == '200': 
              response =  resp.text
              return response
        except: 
           #休息...............................
           os.system("cls") #清除畫面
           print("對方網站封鎖!!休息5分鐘在spider")
           time.sleep(300)
           try:
              headersItems = {
                            'Content-Type' : 'text/html;charset=UTF-8',
                            'Referer' : url,
                            'Upgrade-Insecure-Requests' : '1',
                            'Cookie': self.cookies,
                            'user-agent':  self.useragent 
               }    
              response =""  
              time.sleep(5)      
              resp = requests.get(url, headers=headersItems, timeout=120)
              if str(resp.status_code) == '200': 
                 response =  resp.text
           except:
               return ""



def long_time_task(name,_cookies,_useragent):
   #由目錄開始爬取              
   #取得 TABLE 中目錄數
   ipaddr = comm.get_ip_address()
   
   strSQL = str('select * from db_categoryTemp with(nolock) where m_id=' + str(m_id)  + ' and recno % ' + str(runtimeint) + '='+ str(name) + '  and doflag =0 order by Recno   ')

   goods_conn = pymssql.connect(server=str(sqlserverIP), user='XXX', password='XXX', database='XXX', timeout=2400, login_timeout=600)
   cursor = goods_conn.cursor()
   cursor.execute(strSQL)
   row = cursor.fetchone()
   
   print('收錄目錄: %s ' % (str('recno % ' + str(runtimeint) + '='+ str(name))))
   while row:
         os.system("cls") #清除畫面
         obj = {}
         obj['items'] = []
         posts = []
         page_num = 1
         _newest = 0   
         row_cate_url = str(row[2])
         row_cate_url = row_cate_url.replace(trackcode,'') .replace('%3a%2f%2f',str('://')).replace('%2f',str('/')).replace('%3f',str('?')).replace('%26',str('&')).replace('%3d',str('='))
         cname=""
         print('收錄目錄: %s ' % (str(row_cate_url)))
         #爬取網頁，只能爬取30頁，每頁抓完讓他休息3秒
         cateurl = str(row_cate_url) + str("&page=1")
         row_cate_url =cateurl
         try:
            GTI = GetbooksSpider(cateurl,str(row[2]) ,str(row[3]),str(row[0]),_cookies,_useragent)
         
            updateSQL = str("update db_categoryTemp  set doflag =1,modifydate=getdate(),c_name=N'" + str(GTI.cname) + "'  where m_id='" + str(m_id) + "' and recno =" + str(row[0]))
            comm.CommitTable_dbname(updateSQL,sqlserverIP,"apitemptb")  
         except Exception as e:
                print('spider error: %s ' % (str(e)))
                updateSQL = str("update db_categoryTemp  set doflag =2,modifydate=getdate(),c_name=N'" + str(GTI.cname) + "'  where m_id='" + str(m_id) + "' and recno =" + str(row[0]))
                comm.CommitTable_dbname(updateSQL,sqlserverIP,"apitemptb")                  
                pass          
         #下一個row 
         row = cursor.fetchone()
   start = time.time()
   time.sleep(random.random() * 3)
   end = time.time()
   print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def cd_dvd_task(name,_cookies,_useragent):
   #由目錄開始爬取              
   #取得 TABLE 中目錄數
   ipaddr = comm.get_ip_address()
   if (ipaddr.find(".60") >0) :
      strSQL = str("select * from db_categoryTemp with(nolock) where m_id=" + str(m_id)  + " and (c_name like '%合輯%' or c_name like '%CD＞%' or c_name like '%DVD＞%') and doflag=0 order by recno ")
   else:
      strSQL = str("select * from db_categoryTemp with(nolock) where m_id=" + str(m_id)  + " and (c_name like '%合輯%' or c_name like '%CD＞%' or c_name like '%DVD＞%') and doflag=0 order by recno desc ")

   goods_conn = pymssql.connect(server=str(sqlserverIP), user='XXX', password='XXX', database='XXX', timeout=2400, login_timeout=600)
   cursor = goods_conn.cursor()
   cursor.execute(strSQL)
   row = cursor.fetchone()

   print('收錄目錄: %s ' % (str('recno % 10='+ str(name))))
   while row:
         os.system("cls") #清除畫面
         obj = {}
         obj['items'] = []
         posts = []
         page_num = 1
         _newest = 0   
         row_cate_url = str(row[2])
         row_cate_url = row_cate_url.replace(trackcode,'') .replace('%3a%2f%2f',str('://')).replace('%2f',str('/')).replace('%3f',str('?')).replace('%26',str('&')).replace('%3d',str('='))
         cname=""
         print('收錄目錄: %s ' % (str(row_cate_url)))
         #爬取網頁，只能爬取30頁，每頁抓完讓他休息3秒
         cateurl = str(row_cate_url) + str("&page=1")
         row_cate_url =cateurl
         try:
            GTI = GetbooksSpider(cateurl,str(row[2]) ,str(row[3]),str(row[0]),_cookies,_useragent)
         
            updateSQL = str("update db_categoryTemp  set doflag =1,modifydate=getdate(),c_name=N'" + str(GTI.cname) + "'  where m_id='" + str(m_id) + "' and recno =" + str(row[0]))
            comm.CommitTable_dbname(updateSQL,sqlserverIP,"apitemptb")  
         except Exception as e:
                print('spider error: %s ' % (str(e)))
                updateSQL = str("update db_categoryTemp  set doflag =2,modifydate=getdate(),c_name=N'" + str(GTI.cname) + "'  where m_id='" + str(m_id) + "' and recno =" + str(row[0]))
                comm.CommitTable_dbname(updateSQL,sqlserverIP,"apitemptb")                  
                pass  

         #下一個row 
         row = cursor.fetchone()
   start = time.time()
   time.sleep(random.random() * 3)
   end = time.time()
   print('Task %s runs %0.2f seconds.' % (name, (end - start)))

      
if __name__ == '__main__':
   localDirName ="C:\FP_GOODS\Data\proxies.csv" #proxy ip list

   _useragent = UAT.process_request(__name__)

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
   #chrome_options.add_argument('--headless')#無介面模式 
   driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
   driver.maximize_window()
   driver.implicitly_wait(30) # seconds
   driver.get('https://www.books.com.tw/')
   time.sleep(3) ## delays for 3 seconds

   _cookies = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()])  


   #把剩下沒有匯入的xml檔再執行一次20200910
   ipaddr = comm.get_ip_address()
   xmlfiles = comm.seachpathallfiles(Dstfilename,r'\*.xml')
   xmlfiles1 = comm.seachpathallfiles(Dstfilename,r'\*.xml.error')
   if (len(xmlfiles1)>0) or len(xmlfiles)>0:
      xmlfiles = xmlfiles + xmlfiles1
      for listfiles in xmlfiles: #傳出實體搜尋出的路徑檔案列表
          filesname = comm.getfilename(listfiles) #取得檔案名稱
          try:
              if (comm.isfileExists(listfiles)):#檔案是否存在
                  filenameR = UspApiPatch + "/" + filesname
                  execSQL = "EXEC SetXmlFile2PrimallTemp '" + str(m_id)  + "','" + filenameR + "'"
                  comm.CommitTable_dbname(execSQL,sqlserverIP,"apitemptb")
                  comm.rename2filename(listfiles,listfiles + ".ok")
          except :
               time.sleep(5) #delays for 5 seconds
               try:
                  if (comm.isfileExists(Dstfilename)):
                      filenameR = UspApiPatch + "/" + filesname
                      execSQL = "EXEC SetXmlFile2PrimallTemp '" + str(m_id)  + "','" + filenameR + "'"
                      comm.CommitTable_dbname(execSQL,sqlserverIP,"apitemptb")
                      comm.rename2filename(listfiles,listfiles + ".ok")
               except :
                  comm.rename2filename(listfiles,listfiles + ".error")

   ipaddr = comm.get_ip_address()
   if (ipaddr.find(".60") >0) :
       cd_dvd_task(1,_cookies,_useragent)
 
   #print('Parent process %s.' % os.getpid())
   ## 建立 runtimeint 個子執行緒
   #threads = []
   #for i in range(runtimeint):
   #    threads.append(threading.Thread(target = long_time_task, args = (i,_cookies,_useragent,)))
   #    threads[i].start()

   ## 主執行緒繼續執行自己的工作
   ## 等待所有子執行緒結束
   #for i in range(runtimeint):
   #   threads[i].join()
   #print('等待全部processes 做完...')

   print('Parent process %s.' % os.getpid())
   p = Pool(runtimeint) #定義CPU核心量為3
   for i in range(runtimeint):
       p.apply_async(long_time_task, args=(i,_cookies,_useragent,))
   print('等待全部processes 做完...')
   p.close()
   p.join()
   print('全部p processes 已做完.')

   driver.quit()
   try:
     sys.exit(0)
     os._exit(0)
   except:
    print('Program is dead.')
