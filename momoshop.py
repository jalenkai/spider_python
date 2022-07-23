# -*- coding:utf-8 -*-
#import sys

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

from lxml import etree 
from multiprocessing import Pool
import random
import command as comm
import requests,datetime
import time
import urllib.parse
import json
import threading



sqlserverIP = 'xxx.xxx.xx.xx'
m_id="xx"
setPageCnt =20 #爬取網頁，最多只能爬取20頁(自訂)max

ipaddr = comm.get_ip_address()
UspApiPatch = r"d:\xxx\Data\momoshop"
Dstfilename = r"d:\xxx\Data\momoshop"


filename_save = 0
runtimeint = 10

today2weekday = comm.today2weekday(datetime.date.today())#星期一傳回 1 星期日傳回 7

def closePres():
  #每日06:00排程開啟~23:00自動關閉
  getnow = datetime.datetime.now()
  getnow_hour = int(getnow.hour)
  getnow_minute = int(getnow.minute)
  today2weekday = comm.today2weekday(datetime.date.today())#星期一傳回 1 星期日傳回 7
  if  (getnow_hour==9 and getnow_minute<=30) : #09:30就關閉程序
    try:
     sys.exit(0)
    except:
     print('Program is dead.(sys.exit(0))')

    try:
      os._exit(0)
    except:
      print('Program is dead.(os._exit(0))')

#頭尾切字串
def StartEndStrTrun(Rstr,Startstr,Endstr):
        begint = Rstr.find(Startstr)
        endint = Rstr.find(Endstr)
        if begint <0 :
           begint =0
        if endint <0 : #20220126 當找不到時則取至尾
            endint = len(Rstr) 
        return  str(Rstr[begint:endint].replace(Startstr,''))

class GetmomoshopSpider(object): 
    def __init__(self, cateurl,cname,recno,_cookies,_useragent):       
        self.cookies = _cookies
        self.useragent = _useragent
        self.url = cateurl
        self.cname = cname
        PageTotalCount = self.spiderPageTotalCount(self.url)
        if int(PageTotalCount) > int(setPageCnt):
           self.pageSum = setPageCnt
        else :
            self.pageSum = int(PageTotalCount)  #必須要讀取url總頁數

        if (self.pageSum>0):
           #self.urls = self.getUrls(self.pageSum)
           #if (self.pageSum>0):
           self.spider(recno)
        else:
           print("無資料可讀取!!")

    def getUrls(self,pageSum):
        urls = []
        pagenum = [str((i*1)+1) for i in range(pageSum)]
        ul = self.url.split('&p_pageNum=') #將連結=字串分解
        #先取得第一頁得到總頁數
        for page in pagenum:
            ul[-1] = page
            url = '&p_pageNum='.join(ul) 
            urls.append(url)
        return urls
    
    #傳入第一頁取得總頁次
    def spiderPageTotalCount(self,url):
        os.system("cls") #清除畫面
        print("取得資料,調用api!!")
        d_code =comm.StartEndStrTrun(url,'?d_code=','&')
        timeStamp  = int(round(time.time() * 1000))  #13碼時間戳
        apiurl='https://www.momoshop.com.tw/ajax/ajaxTool.jsp?n=2035' + str(timeStamp) #&t=1643162298549
        
        result_Items = 'data=' + urllib.parse.quote(str('{"flag":2035,"data":{"params":{"keyword":"","checkedBrands":[],"checkedBrandsNo":[],"checkedAttrs":{},"checkedAttrsNo":{},"isBrandZone":false,"specialGoodsType":"","cateCode":"'+ d_code +'","cateLevel":"3","cp":"N","NAM":"N","normal":"N","first":"N","freeze":"N","superstore":"N","tvshop":"N","china":"N","tomorrow":"N","stockYN":"N","prefere":"N","threeHours":"N","curPage":"1","priceS":"","priceE":"","brandName":[],"sortType":"6","d_code":"'+ d_code +'","p_orderType":"6","showType":"chessboardType"}}}' ))
        
        try:           
            headers = {
                      'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                      'Accept' : 'application/json, text/javascript, */*; q=0.01',
                      'X-Requested-With' : 'XMLHttpRequest',
                      'referer': url,    
                      'Cookie': _cookies,
                      'user-agent': _useragent 
                                            }
            pagecnt =0
            res = requests.post(apiurl,data = result_Items, headers = headers, timeout=1200) 
            if str(res.status_code) == '200': 
              print("取得%s資料目錄總頁次" % (str(url)))
              prods = json.loads(res.text.replace('\n',''))
              pagecnt = int(prods['rtnData']['rtnGoodsData']['maxPage'])
              print("取得 %s ,共: %d 頁" % (str(url) , pagecnt))
            return pagecnt
        except: 
              return pagecnt          
          
    def spider(self,recno):    
        pagecnt = 0
        #定義xml格式
        _root = etree.Element("productList") 
        for curPage in range(self.pageSum): 
            pagecnt +=1
            time.sleep(2) 
            os.system("cls") #清除畫面
            print("取得商品資料,調用api!!")
            d_code =comm.StartEndStrTrun(self.url,'?d_code=','&')
            timeStamp  = int(round(time.time() * 1000))  #13碼時間戳
            apiurl='https://www.momoshop.com.tw/ajax/ajaxTool.jsp?n=2035' + str(timeStamp) #&t=1643162298549
            
            result_Items = 'data=' + urllib.parse.quote(str('{"flag":2035,"data":{"params":{"keyword":"","checkedBrands":[],"checkedBrandsNo":[],"checkedAttrs":{},"checkedAttrsNo":{},"isBrandZone":false,"specialGoodsType":"","cateCode":"'+ d_code +'","cateLevel":"3","cp":"N","NAM":"N","normal":"N","first":"N","freeze":"N","superstore":"N","tvshop":"N","china":"N","tomorrow":"N","stockYN":"N","prefere":"N","threeHours":"N","curPage":"' + str(pagecnt) + '","priceS":"","priceE":"","brandName":[],"sortType":"6","d_code":"'+ d_code +'","p_orderType":"6","showType":"chessboardType"}}}' ))
            #try:
            headers = {
                      'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                      'Accept' : 'application/json, text/javascript, */*; q=0.01',
                      'X-Requested-With' : 'XMLHttpRequest',
                      'referer': self.url,    
                      'Cookie': _cookies,
                      'user-agent': _useragent 
                                            }          
            res = requests.post(apiurl,data = result_Items, headers = headers, timeout=1200) 
            if str(res.status_code) == '200':
                   print("取得商品資料status_code=%s" % (str(res.status_code)))
                   cntint=0
                   prods = json.loads(res.text.replace('\n',''))
                   for goodsdata in prods['rtnData']['rtnGoodsData']['rtnGoodsData']['goodsInfoList']:
                       #goodsStock : 商品庫存(Availability) ; goodsSubName :促銷小標 (goodsbrief) ; SALE_PRICE 促銷價 ->goodsPrice comm.gprice() : (ProductSalePrice)
                       #goodsurl:https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=[goodsCode] (BuyURL)
                       #imgUrl(ProductImage2),goodsName(ProductName): 
                       #goodsCode(ProductID)
                       ProductID = str(goodsdata['goodsCode'])
                       BuyURL = str('https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=') + str(ProductID)
                       if (BuyURL.find(str('?')) >= 0):
                          BuyURL =  BuyURL + str('&') + str(trackcode)
                       else :
                          BuyURL =  BuyURL + str('?') + str(trackcode)
                       try:
                          ProductName = comm.getbrief(str(goodsdata['goodsName']))
                       except: 
                           ProductName =""

                       try:
                          imgUrl = str(goodsdata['imgUrl'])
                          imgUrl = imgUrl.replace(".webp", ".jpg")
                       except: 
                           imgUrl =""

                       if (str(goodsdata['goodsStock'])!=''):
                          Availability = str(goodsdata['goodsStock'])#商品庫存

                       try:
                          ProductSalePrice =comm.getprice(goodsdata['goodsPrice'])
                       except: 
                          ProductSalePrice =comm.getprice(goodsdata['SALE_PRICE'])
                          SalePrice =comm.getprice(goodsdata['SALE_PRICE'])

                       try:
                          SalePrice =comm.getprice(goodsdata['SALE_PRICE'])
                       except: 
                          ProductSalePrice =comm.getprice(goodsdata['goodsPrice'])
                          SalePrice =comm.getprice(goodsdata['goodsPrice'])

                       ProductDescription=""
                       try:
                          if  (goodsdata['goodsSubName']!=''):
                             ProductDescription = goodsdata['goodsSubName'] 
                             re_han_1 = re.findall("滿[0-9]+[\u4E00-\u9FD5]+",ProductDescription)#滿1件享???
                             re_han_2 = re.findall("[0-9]+折",ProductDescription) #??折
                             if (len(re_han_1) >0 or len(re_han_2) >0) :
                                ProductDescription = comm.getbrief(str(goodsdata['goodsSubName']))
                             else:
                               ProductDescription=""
                       except: 
                           ProductDescription=""

                       if (int(Availability)==0 or SalePrice==0 or imgUrl=='' or ProductName=='' or BuyURL==''):
                           print("商品不匯入!!")
                           continue

                       cntint +=1
                       os.system("cls") #清除畫面
                       print('目前抓取目錄:%s' % (str(self.url)))
                       print('共%d頁，目前正在抓取第 %d 頁資料第 %d 筆' % (int(self.pageSum),int(pagecnt),int(cntint))) 
                       try:
                              #開始匯入商品資料
                              _body = etree.SubElement(_root,"Products") 
                              etree.SubElement(_body, "ProductID").text =  etree.CDATA(str(ProductID))   
                              etree.SubElement(_body, "ProductName").text = etree.CDATA(str(ProductName)) 
                              etree.SubElement(_body, "BuyURL").text = etree.CDATA(str(BuyURL))
                              etree.SubElement(_body, "ProductImage").text = etree.CDATA(str(imgUrl))
                              etree.SubElement(_body, "ProductSalePrice").text = etree.CDATA(str(ProductSalePrice))
                              etree.SubElement(_body, "SalePrice").text = etree.CDATA(str(SalePrice))
                              etree.SubElement(_body, "cate_recno").text = etree.CDATA(str(recno))
                              etree.SubElement(_body, "CategoryURL").text = etree.CDATA(str(self.url))
                              etree.SubElement(_body, "CategoryName").text = etree.CDATA(str(self.cname))
                              etree.SubElement(_body, "ProductDescription").text = etree.CDATA(str(ProductDescription)) 
                       except: 
                                print("xml異常,error")
            #except: 
            #     print("status_code=%s" % (str(res.status_code)))

        #2.存成xml檔案 
        tree = etree.ElementTree(_root)
        filename = str(Dstfilename + '\momoshop' +  str(recno) + '.xml')
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        #直接存入SQL
        if (os.path.exists(filename)):
           try:
                 filenameR = str('D:\xxx\Data\momoshop\momoshop' + str(recno) + '.xml')   
                 #彙整至 [apitemptb].[dbo].db_momoproductList_xml_spider 
                 execSQL = "EXEC SetXmlFile2PrimallTemp '14_1','" + filenameR + "'"

                 comm.CommitTable_dbname(execSQL,sqlserverIP,"xxx")
                 os.rename(filename,filename + ".ok")
           except:
                 os.rename(filename,filename + ".error.ok") 

    #GET
    #@with_goto
    def getResponseContent(self,url):
        #label .myLoopc
        try:   
           http = urllib3.PoolManager()
           headersItems = {
                            'Content-Type' : 'text/html;charset=UTF-8',
                            'Cookie': self.cookies,
                            'user-agent':  self.useragent 
           }  
           response = http.request('GET', url, headers = headersItems)
           time.sleep(1)
        except: 
           #休息...............................
           time.sleep(2)
           print("連結錯誤!!")
           #goto .myLoopc
        else:
           return response.data


def long_time_task(name,_cookies,_useragent):
    #print('Run task %s (%s)...' % (name, os.getpid()))
   #由目錄開始爬取              
   #取得 TABLE 中目錄數
   ipaddr = comm.get_ip_address()
   if (ipaddr.find(".60") >0) :
      strSQL = str('select recno,c_link,c_name from db_categoryTemp with(nolock) where m_id=' + str(m_id)  + ' and recno % ' + str(runtimeint) + '='+ str(name) + '  and doflag =0 order by newid(),Recno   ')
   else:
      strSQL = str('select recno,c_link,c_name from db_categoryTemp with(nolock) where m_id=' + str(m_id)  + ' and recno % ' + str(runtimeint) + '='+ str(name) + '  and doflag =0 order by newid(),Recno  desc ')

   if int(name)<0 :
      strSQL = str('select recno,c_link,c_name from db_categoryTemp with(nolock) where m_id=' + str(m_id)  + ' and doflag =0 order by Recno ')

   goods_conn = pymssql.connect(server=str(sqlserverIP), user='xx', password='xx', database='xxx', timeout=2400, login_timeout=600)  #
   cursor = goods_conn.cursor()
   cursor.execute(strSQL)
   row = cursor.fetchone()
   #每一目錄只能爬行100頁限制
   filename_save = 1
   print('收錄目錄: %s ' % (str('recno % 10='+ str(name))))
   while row:
         os.system("cls") #清除畫面
         obj = {}
         obj['items'] = []
         posts = []
         page_num = 1
         _newest = 0   
         cateurl = str(row[1])  
         print('收錄目錄: %s ' % (str(cateurl)))

         closePres()#遇到上午 09 點就關閉不做由排程執行
         try:
            GTI = GetmomoshopSpider(cateurl,str(row[2]),str(row[0]),_cookies,_useragent)
         
            updateSQL = str('update db_categoryTemp  set doflag =1,modifydate=getdate()  where m_id=' + str(m_id) + ' and recno =' + str(row[0]))   
            comm.CommitTable_dbname(updateSQL,sqlserverIP,"xxx")
         except: 
             pass
         
         #下一個row 
         row = cursor.fetchone()


def isGetCatTemp():
   strSQL = str("select cnt=count(*) from db_categoryTemp where m_id='" + str(m_id)+ "' and doflag=0 ")
   cntdoflag = comm.getFildValue(strSQL,sqlserverIP,0,"xxx")
   if (cntdoflag=="0"):
      return True
   else: 
      return False

    #GET
def getResponseContent(url,_Referer):
    response = ""
    try:   
       if _Referer!= '':   
          headersItems = {
                        'content-type' : 'application/json; charset=utf-8',
                        'Cookie': _cookies,
                        'Referer':_Referer,
                        'user-agent':  _useragent 
         } 
       else:
          headersItems = {
                        'content-type' : 'application/json; charset=utf-8',
                        'Cookie': _cookies,
                        'user-agent':  _useragent 
         } 
       time.sleep(1)  
       
       resp = requests.get(url=url,headers=headersItems, timeout=1200)#分析得出的網址 
       if str(resp.status_code) == '200': 
            response =  resp.text         
    except: 
       print("連結錯誤!!")
    
    return response

#取目錄
def GetCateData(url):
    htmlContent = getResponseContent(url,'https://www.momoshop.com.tw/')
    if (htmlContent!=""):        
        soup = BeautifulSoup(htmlContent, 'lxml')
        time.sleep(2)  
        for itemText in soup.find_all('ul', attrs={'class':'navcontent_listul'})[0].find_all('li'):
            try:
                os.system("cls") #清除畫面
                c_name_l_code0 = itemText.attrs['l_code']
                c_name0 = itemText.text #第0層 
                print('取得目錄: %s , %s 目錄l_code' % (str(c_name0),str(c_name_l_code0)))
                ##test##################
                #if c_name0=='3C' or c_name0=='家電': 
                #   continue
                ########################
                for l_codelist in c_name_l_code0.split(','): #每個第0層 l_code 逐一 找尋
                    for menu1 in soup.find_all('table', attrs={'class':'topmenu'}): #由目錄層root找
                        for menu1_td in menu1.find_all('td'):
                            #每個td包所屬的資料 每個第0層 l_code 第1層  資料
                            if menu1_td.contents[1].attrs['l_code']==str(l_codelist):
                               c_name1 =  menu1_td.p.text #第1層
                               for menu1_td_p in menu1_td.contents[3].find_all('li'):#由第1層資料,取出第2層資料
                                   c_link2 = menu1_td_p.a['href'] #第2層 可取得(品牌)
                                   c_name2 = menu1_td_p.text

                                   if (c_name2.find('閱讀/文學')>=0) or (c_name2.find('知識/理財')>=0): 
                                      continue

                                   dchk = True
                                   if c_link2.find('DgrpCategory.jsp')>=0:#最後一層c_link
                                      d_code = comm.StartEndStrTrun(c_link2,'?d_code=','&') #當沒有'&'時會少一碼 
                                      c_link = 'https://www.momoshop.com.tw/category/DgrpCategory.jsp?d_code=' + str(d_code)                                                         
                                      c_name =  c_name1 + '＞' + c_name2 
                                      os.system("cls") #清除畫面
                                      print('新增momoshop第4層目錄%s...' % (str(c_link)))
                                      strSQL =  "INSERT INTO [dbo].[db_PricateTemp] ([m_id],[cateUrl],[cate_name],[cate_Root],[createdate],[modifydate])"
                                      strSQL +=  " VALUES ('" + str(m_id) + "','" + str(c_link)  + "',N'" + str(c_name)  + "','4',getdate(),getdate()) "
                                      comm.CommitTable_dbnameTimeout(strSQL,sqlserverIP,"xxx",3600)
                                      dchk =False
                                       
                                   #l_code=1912900000&mdiv=1099600000-bt_0_996_10-&ctype=B"
                                   l_code2 =comm.StartEndStrTrun(c_link2,'l_code=','&mdiv')
                                   timeStamp  = int(round(time.time() * 1000))  #13碼時間戳
                                   apiurl= 'https://www.momoshop.com.tw/ajax/ajaxTool.jsp?n=2022&t=' + str(timeStamp)
                                   print('取得momoshop品牌總覽資料brandName...')
   
                                   result_Items = 'data=' + urllib.parse.quote(str('{"flag":2022,"data":{"params":{"cateCode":"'+ l_code2 +'","cateLevel":"1","cp":"N","NAM":"N","normal":"N","first":"N","freeze":"N","superstore":"N","tvshop":"N","china":"N","tomorrow":"N","stockYN":"N","prefere":"N","threeHours":"N","curPage":"1","priceS":"0","priceE":"9999999","brandName":[],"searchType":"6"}}}' ))
                                   try :
                                       headers = {
                      'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                      'Accept' : 'application/json, text/javascript, */*; q=0.01',
                      'X-Requested-With' : 'XMLHttpRequest',
                      'referer': c_link2,    
                      'Cookie': _cookies,
                      'user-agent': _useragent 
                                            }
   
                                       res = requests.post(apiurl,data = result_Items, headers = headers, timeout=1200) 
                                       if str(res.status_code) == '200': 
                                          prods = json.loads(res.text.replace('\n',''))
                                          inscnt=0
                                          print('開始匯入momoshop品牌總覽資料brandName資料!!')
                                          for brandName in prods['rtnData']['searchResult']['rtnSearchData']['brandNameList']:
                                              brandName = comm.getbrief(brandName['brandName'])
                                              #匯入 jieba_dict add sortid=89
                                              for brandName_sp in brandName.split(' '):
                                                  if len(brandName_sp)>1:
                                                     insdatesql = "INSERT INTO  jieba_dict ([keyword],[weights],[vtype],[sortid],[modifydate]) "
                                                     strSQL = " SELECT insertdb.[keyword],insertdb.[weights],insertdb.[vtype],insertdb.[sortid],insertdb.[modifydate] "
                                                     strSQL += " FROM (SELECT keyword=N'" + str(brandName_sp.replace("'","''").replace('"',"''")) + "',weights='200',vtype='N',sortid='89',modifydate=getdate()) AS insertdb "
                                                     strSQL += " LEFT JOIN dbo.real_keyword_temp  b with(nolock) ON insertdb.keyword = b.Key_name "
                                                     strSQL += " WHERE b.Key_name IS NULL and not  exists(select 1 from [goodsTemp].[dbo].[jieba_dict] jbd with(nolock)  where jbd.keyword=insertdb.keyword) "

                                                     insdatesql += strSQL
                                                     if comm.CommitTable_dbnameTimeout(insdatesql,"xxx.xxx.xxx.xxx","xxx",1200)==1 :
                                                        strSQL = str("select cnt=count(*) from (" + strSQL + ")a")
                                                        cntdoflag = comm.getFildValue(strSQL,"xxx.xxx.xxx.xxx",0,"xxx")
                                                        if int(cntdoflag) >0 :
                                                           inscnt +=1
                                                           print('匯入(品牌總覽資料brandName) %d 筆' % (inscnt))

                                   except :
                                        print('momoshop價格api讀取異常!!')

                                   if (dchk==False):
                                       print('已經是底層!!')
                                       continue

                                   print('取得momoshop第3層目錄...')
                                   htmlContent3 = getResponseContent(c_link2,'https://www.momoshop.com.tw/')
                                   if (htmlContent3!=""):        
                                       soup3 = BeautifulSoup(htmlContent3, 'lxml')
                                       time.sleep(2) 
                                       c_name3 =""
                                       for itemText3 in soup3.find_all('ul', attrs={'id':'bt_cate_top'})[0].find_all('li'):
                                               #判斷是否為第3層目錄
                                               try:
                                                  itemText3_li_M =  itemText3.attrs['class'][0]
                                                  if itemText3_li_M=='cateM':
                                                     c_name3 =  c_name1 + '＞' + c_name2 + '＞' + comm.getbrief(itemText3.contents[0].text)
                                                     if (c_name3.find('閱讀/文學')>=0) or (c_name3.find('知識/理財')>=0): 
                                                          continue

                                                  elif itemText3_li_M=='cateS':
                                                     href_link = itemText3.find('a')['href']
                                                     href_name = comm.getbrief(itemText3.find('a').text)
                                                     if href_link.find('DgrpCategory.jsp')>0:#最後一層c_link
                                                        d_code = comm.StartEndStrTrun(href_link,'?d_code=','&') #當沒有'&'時會少一碼 
                                                        c_link = 'https://www.momoshop.com.tw/category/DgrpCategory.jsp?d_code=' + str(d_code)                                                         
                                                        c_name =  c_name3 + '＞' + href_name
                                                        os.system("cls") #清除畫面
                                                        print('新增momoshop第4層目錄%s...' % (str(c_link)))
                                                        strSQL =  "INSERT INTO [dbo].[db_PricateTemp] ([m_id],[cateUrl],[cate_name],[cate_Root],[createdate],[modifydate])"
                                                        strSQL +=  " VALUES ('" + str(m_id) + "','" + str(c_link)  + "',N'" + str(c_name)  + "','4',getdate(),getdate()) "
                                                        comm.CommitTable_dbnameTimeout(strSQL,sqlserverIP,"xxx",3600)
                                               except :
                                                   pass
            except:
                pass


#20220221 BY JALEN 將異常沒有收錄的XML檔轉入,並更新db_categoryTemp
def setFiles2TempDB():
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
                  comm.CommitTable_dbnameTimeout(execSQL,sqlserverIP,"xxx",1200)
                  comm.rename2filename(listfiles,listfiles + ".ok")

                  #更新db_categoryTemp
                  recno = filesname.replace('momoshop','').replace('.xml','').replace('xml','')
                         
                  updateSQL = str('update db_categoryTemp with(rowlock) set doflag =1,modifydate=getdate()  where m_id=' + str(m_id) + ' and recno =' + str(recno))   
                  comm.CommitTable_dbnameTimeout(updateSQL,sqlserverIP,"xxx",1200)
          except :
               time.sleep(5) #delays for 5 seconds
               try:
                  if (comm.isfileExists(Dstfilename)):
                      filenameR = UspApiPatch + "/" + filesname
                      execSQL = "EXEC SetXmlFile2PrimallTemp '" + str(m_id)  + "','" + filenameR + "'"
                      comm.CommitTable_dbnameTimeout(execSQL,sqlserverIP,"xxx",1200)
                      comm.rename2filename(listfiles,listfiles + ".ok")

                      #更新db_categoryTemp
                      recno = filesname.replace('momoshop','').replace('.xml','').replace('xml','')
                         
                      updateSQL = str('update db_categoryTemp with(rowlock) set doflag =1,modifydate=getdate()  where m_id=' + str(m_id) + ' and recno =' + str(recno))   
                      comm.CommitTable_dbnameTimeout(updateSQL,sqlserverIP,"xxx",1200)
               except :
                  comm.rename2filename(listfiles,listfiles + ".error")

if __name__ == '__main__':      
   #chrome_options = webdriver.ChromeOptions()
   #chrome_path = "C:\selenium_driver\chromedriver.exe"
   #chrome_options.add_argument('--headless')#無介面模式 
   #driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
   firefox_options = webdriver.FirefoxOptions()
   firefox_path = "C:\selenium_driver\geckodriver.exe"
   firefox_options.add_argument('--headless')#無介面模式
   driver = webdriver.Firefox(executable_path=firefox_path,firefox_options=firefox_options)

   driver.implicitly_wait(50) # seconds
   driver.get('https://www.momoshop.com.tw/')
   time.sleep(3) ## delays for 3 seconds

   _cookies = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()])
   _useragent = UAT.process_request(__name__)
   if ( _cookies!=""  ):
      driver.quit()


   setFiles2TempDB()
   comm.chkPatchDelFilesAll(Dstfilename , "momoshop*.ok") #刪除xml暫存檔   

   if (isGetCatTemp()==True): #爬目錄############################
      if today2weekday==6 or today2weekday==7 :
         #存入categorydict     
         GetCateData('https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=4301100000')

   getnow = datetime.datetime.now()
   getnowhour = int(getnow.hour)#一日的開始,必須初始化
    
   #由categorydict 取出爬
   print('Parent process %s.' % os.getpid())
   # 建立 runtimeint 個子執行緒
   threads = []
   for i in range(runtimeint):
          threads.append(threading.Thread(target = long_time_task, args = (i,_cookies,_useragent,)))
          threads[i].start()

      # 主執行緒繼續執行自己的工作
      # 等待所有子執行緒結束
   for i in range(runtimeint):
         time.sleep(5)
         threads[i].join()
   print('等待全部processes 做完...')

   setFiles2TempDB()
   comm.chkPatchDelFilesAll(Dstfilename , "momoshop*.ok") #刪除xml暫存檔   


   try:
      driver.quit()
      sys.exit(0)
   except:
       print("close")

   try:
     os._exit(0)
   except:
       print("close")



        

    
