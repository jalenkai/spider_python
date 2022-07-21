

import time
import os
import json
import requests
from fake_useragent import UserAgent
import command as comm
import datetime
import pandas as pd
from google.cloud import bigquery as bq

sqlserverIP ="xxx.xxx.xxx.xxx"
m_id = "101"
ipaddr = comm.get_ip_address()
UspApiPatch = r"C:\xxx\Data\klook"
Dstfilename =  r"C:\xxx\Data\klook"

maxPageCnt = 350 #最大收錄頁數

runtimeint = 0
runEndPage = 0 

class GetklookSpider(object):
    def __init__(self,m_id):
        ua = UserAgent()
        _useragent = ua.google

        self.m_id = m_id
        today2weekday = comm.today2weekday(datetime.date.today())  # 星期一傳回 1 星期日傳回 7
        category_data = pd.DataFrame({
            "c_name": ["玩樂", "度假專案", "機場鐵路＆巴士", "租機車＆重機", "交通票券"],
            "c_link": [
                "https://www.klook.com/zh-TW/experiences/mcate/1-%e7%8e%a9%e6%a8%82/activity/?frontend_id_list=1&size=24&page=1",
                "https://www.klook.com/zh-TW/search/?frontend_id_list=55&start=1",
                "https://www.klook.com/zh-TW/search/?frontend_id_list=49&start=1",
                "https://www.klook.com/zh-TW/search/?frontend_id_list=52&sort=participants&start=1",
                "https://www.klook.com/zh-TW/search/?frontend_id_list=50&sort=participants&start=1"],
            "apiurl": ["https://www.klook.com/v1/experiencesrv/category/activity?frontend_id_list=1&size=24&start=[pno]",
                       "https://www.klook.com/v2/usrcsrv/search/all_activities?frontend_id_list=55&size=24&start=[pno]",
                       "https://www.klook.com/v2/usrcsrv/search/all_activities?frontend_id_list=49&size=24&start=[pno]",
                       "https://www.klook.com/v2/usrcsrv/search/all_activities?frontend_id_list=52&size=24&start=[pno]",
                       "https://www.klook.com/v2/usrcsrv/search/all_activities?frontend_id_list=50&size=24&start=[pno]"]
        })
        self.useragent = _useragent
        self.chkdata = True

        self.spider(category_data)


    def spider(self,category_data):
            self.chkdata = False
            credentials_path = r'C:\googleapi\gcxxx.json' #gc驗證檔
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

            client = bq.Client()
            dataset_id = 'findprice-354106.goods_spider'  # 設定 Dataset 名稱，可以修改(資料集)
            dataset = bq.Dataset(dataset_id)
            #creat dataset
            # dataset.location = "asia-east1"  # 設定資料位置，如不設定預設是 US
            # dataset.default_table_expiration_ms = 30 * 24 * 60 * 60 * 1000  # 設定資料過期時間，這邊設定 30 天過期
            # dataset.description = 'creat_new_dataset & expiration in 30 days & location at asia-east1'  # 設定 dataset 描述
            # client.delete_dataset(
            #     dataset_id, delete_contents=True, not_found_ok=True
            # )  # Make an API request.
            # print("Deleted dataset '{}'.".format(dataset_id))

            table_id = 'findprice-354106.goods_spider.db_spiderpricetemp'
            #`findprice-354106.goods_spider.db_spiderpricetemp`
            #query_delete =  ("""DELETE  FROM `findprice-354106.goods_spider.db_spiderpricetemp` WHERE  m_id=101;""")
            query_delete = (
                " DELETE  FROM  `findprice-354106.goods_spider.db_spiderpricetemp` "
                " WHERE m_id=101 ")

            # Set use_legacy_sql to True to use legacy SQL syntax.
            job_config = bq.QueryJobConfig(use_legacy_sql=True)
            # Start the query, passing in the extra configuration.
            query_job = client.query(query_delete, job_config=job_config)

            try:
                #create_table
                # 設定 Table 資料結構
                schema = [
                    bq.SchemaField("m_id", "INTEGER"),
                    bq.SchemaField("g_link", "STRING"),
                    bq.SchemaField("g_name","STRING"),
                    bq.SchemaField("g_image", "STRING"),
                    bq.SchemaField("g_price", "STRING"),
                    bq.SchemaField("c_link", "STRING"),
                    bq.SchemaField("c_name", "STRING"),
                    bq.SchemaField("g_desc", "STRING"),
                    bq.SchemaField("storeurl", "STRING"),
                    bq.SchemaField("storename", "STRING"),
                ]
                table = bq.Table(table_id, schema=schema)
                # 設定 Table 過期時間
                table.expires = datetime.datetime.now() + datetime.timedelta(days=6)
                # 設定 Table 描述
                table.description = "過期時間 6day"
                # 設定 Table Partition
                #table.time_partitioning = bq.TimePartitioning(type_=bq.TimePartitioningType.DAY,field="timestamp",  # name of column to use for partitioningexpiration_ms = 7776000000,)
                # 建立 Table
                table = client.create_table(table)  # Make an API request.
            except Exception as ex:
                print("已有資料表存在!!")

            recno =0
            for itemno in range(len(category_data)):
                recno +=1
                c_name =category_data.loc[itemno]['c_name']
                c_link = category_data.loc[itemno]['c_link']
                apiurl = category_data.loc[itemno]['apiurl']
                print('取得目錄:%s' % (str(c_name)))
                json_dict = []  # 累加 dict 將此目錄所有收錄到的 products 列傳入json_dict_arr[]
                json_dict_arr = []  # 累加 dict 將此目錄所有收錄到的 products 列傳入json_dict_arr[]
                total_cnt= 0
                #if c_link.find('frontend_id_list=1') > 0 :#玩樂
                get_c_link = c_link #c_link.replace('[pno]', str(1))
                get_apiurl = apiurl.replace('[pno]', str(1))
                contentsHtml = getResponseContent(get_apiurl, get_c_link, self.useragent)
                json_object = json.loads(contentsHtml)
                totalg = json_object['result']['total']
                maxPageCnt = int(comm.getFloat45(0, int(totalg) / 24, 0))
                os.system("cls")  # 清除畫面
                print('目錄c_link %s:,共%d頁' % (str(get_c_link), int(maxPageCnt)))
                if c_link.find('frontend_id_list=1') > 0:  # 玩樂
                    urls = self.getUrls(get_c_link,maxPageCnt+1,'&page=',1)#取出要spider的url
                else:
                    urls = self.getUrls(get_c_link, maxPageCnt+1, '&start=', 1)

                pagecnt =0
                for get_c_link in urls :  #20220704 共有325頁
                       ua = UserAgent()
                       self.useragent = ua.google#
                       os.system("cls")  # 清除畫面
                       pagecnt =int(pagecnt+1)

                       #get_c_link = c_link.replace('[pno]',str(pagecnt))
                       get_apiurl = apiurl.replace('[pno]', str(pagecnt))
                       print('目前收錄共%d頁,目前收錄第%d頁,收錄url:%s' % (int(maxPageCnt),int(pagecnt), str(get_c_link)))
                       if pagecnt>1:  break;#test

                       contentsHtml = getResponseContent(get_apiurl,get_c_link,self.useragent)
                       if contentsHtml!="":
                          json_object = json.loads(contentsHtml)
                          try:  # 將此頁所有商品列傳入json_dict[]:24筆
                              json_dict.append(json_object['result']['activities'])
                              gcnt =len(json_object['result']['activities'])
                              total_cnt += gcnt  # 總商品數
                              if gcnt>0:
                                 print('目前收錄共%d筆,收錄url:%s' % (int(total_cnt), str(get_c_link)))
                              else:
                                  print('此目錄無商品資訊(error),收錄url:%s' % (str(get_c_link)))
                          except Exception as ex:
                              print(ex)
                              break

                if len(json_dict)==0:#
                      break
                # 累加 dict 將此目錄所有收錄到的 products 列傳入json_dict_arr[]
                json_dict_arr = []

                for p_dict in range(len(json_dict)):
                       for p_dict_value in range(len(json_dict[p_dict])):#取出每筆資訊
                           df_products = json_dict[p_dict][p_dict_value]#每一筆商品資料
                           df_goodsall = dict()
                           for key, value in df_products.items():  # 更新內容
                              if key == 'sell_price':
                                  try:
                                      g_price = value['amount_display']
                                      g_price = comm.getprice(g_price)
                                  except :
                                      g_price = comm.getprice(value)
                              if key == 'deep_link':
                                 if value.find('https://www.klook.com')<0:
                                     df_products[key] = 'https://www.klook.com' + value
                              if key == 'title':
                                  df_products[key] = comm.getbrief(value.replace('"', "&quot;"))
                                  df_products[key] = comm.getbrief(value.replace('"', "&apos;"))
                              if  key=='deep_link' or key=='title' or key=='sell_price' or key=='image_src' :
                                  if key=='sell_price':
                                      df_goodsall.setdefault('g_price', str(g_price))
                                  elif key=='deep_link':
                                      df_goodsall.setdefault('g_link', df_products[key])
                                  elif key == 'title':
                                      df_goodsall.setdefault('g_name', df_products[key])
                                  elif key == 'image_src':
                                      df_goodsall.setdefault('g_image', df_products[key])
                           # add 自訂內容josn urls, c_name
                           df_goodsall.setdefault('c_link', c_link.replace('&page=[pno]',''))
                           df_goodsall.setdefault('c_name', comm.getbrief(c_name))
                           df_goodsall.setdefault('m_id', int(self.m_id))
                           df_goodsall.setdefault('g_desc', '')
                           df_goodsall.setdefault('storeurl', '')
                           df_goodsall.setdefault('storename', '')
                           json_dict_arr.append(df_goodsall)

                df = pd.DataFrame(json_dict_arr, columns=['m_id','g_link', 'g_name', 'g_image' , 'g_price',
                                                     'c_link', 'c_name','g_desc','storeurl','storename'])
                job = client.load_table_from_dataframe(df, table_id)
                job.result()  # 等待寫入完成
                # 存檔處理###############################################################
                # if len(json_dict_arr) > 0:
                #     self.chkdata = True
                #     jsonArr = json.dumps(json_dict_arr, ensure_ascii=True)
                #     filename = 'klook_' + str(recno) + '.json'
                #     ipaddr = comm.get_ip_address()
                #     if (ipaddr.find(".60") > 0):
                #         zSaveFileAtPath = UspApiPatch + filename
                #     else:
                #         zSaveFileAtPath = 'E:\\Data\\klook\\' + filename
                #     fn = open(zSaveFileAtPath, 'w', encoding="utf-8")  # 存入json檔案######
                #     fn.writelines(str(jsonArr))
                #     fn.close()
                # else:
                #     self.chkdata = False

    # 串頁次連結供spider
    def getUrls(self, c_link,pageSum,splstr,sno=0):
        urls = []
        pagenum = [str(((i - 1) * 1) + 1) for i in range(sno,pageSum)]  # page由0開始....end
        ul = c_link.split(splstr)  # 將連結=字串分解
        # 先取得第一頁得到總頁數
        for page in pagenum:
            ul[-1] = page
            url = splstr.join(ul)
            urls.append(url)
        return urls


def getResponseContent(url,referer,_useragent):
        try:
           headersItems = {
                            'content-Type' : 'text/html;charset=UTF-8',
                            'accept' : 'application/json, text/plain, */*',
                            'referer': referer,
                            'accept-language':'zh_TW',
                            'cookie': 'klk_currency=TWD; kepler_id=47d4c98e-c974-4a4b-ac53-96a8b5613720; persisted_source=www.google.com; k_tff_ch=google_sem; _gcl_aw=GCL.1656051867.EAIaIQobChMIoc6-97nF-AIVir2WCh3segq7EAAYASAAEgIrJvD_BwE; _gcl_dc=GCL.1656051867.EAIaIQobChMIoc6-97nF-AIVir2WCh3segq7EAAYASAAEgIrJvD_BwE; _gcl_au=1.1.70896154.1656051867; gc_tag=gclid%3DEAIaIQobChMIoc6-97nF-AIVir2WCh3segq7EAAYASAAEgIrJvD_BwE; __lt__cid=4f410a7a-9bbb-4815-a518-80e7cd0f4247; __lt__cid.c83939be=4f410a7a-9bbb-4815-a518-80e7cd0f4247; __lt__sid=39a29b43-68c17417; __lt__sid.c83939be=39a29b43-68c17417; _gid=GA1.2.365217574.1656051868; _gac_UA-86696233-17=1.1656051868.EAIaIQobChMIoc6-97nF-AIVir2WCh3segq7EAAYASAAEgIrJvD_BwE; __dbl__pv=6; dable_uid=57378281.1656051867937; _tt_enable_cookie=1; _ttp=6ddcc431-28fc-46d1-9e9d-c277c8d02730; _gac_UA-181637923-2=1.1656051868.EAIaIQobChMIoc6-97nF-AIVir2WCh3segq7EAAYASAAEgIrJvD_BwE; JSESSIONID=ED9F5FF3DB79BEF669650D2BB9E83FEB; KOUNT_SESSION_ID=ED9F5FF3DB79BEF669650D2BB9E83FEB; _clck=r9m3db|1|f2l|0; clientside-cookie=db3f7cc995a4d54a6cf3814be131fad82f631120a45a2de14a1707327190bcd243a939cca02c638171b1508140f69658cc36ae47be06e84943236dfe98b077431b166f4d8db4d37dbc3cf58bc6327b85ccdcbcb7d3f1378a8bb8d65b715e383ab6ec8c659b9ee10f4ea103fd8b6ce74c82812574bd7ca2db72a12f1179da079f444fb87c8e35c0b687f08ec26f686961dd523de4214ab416a7c128; _gac_UA-86696233-1=1.1656051875.EAIaIQobChMIoc6-97nF-AIVir2WCh3segq7EAAYASAAEgIrJvD_BwE; traffic_retain=true; _dc_gtm_UA-86696233-1=1; webp_support=1; _dc_gtm_UA-86696233-17=1; forterToken=0d1d4b236e4c48b39cb6f1538536584b_1656052846899__UDF43_13ck; _clsk=1jq16gp|1656052848497|7|0|e.clarity.ms/collect; datadome=e5rFGVS0a1LwI2ihV~pBNHZTHqH_QPK31bGJXE.U5hMJPPadnZVM.6IO720pdKRXgTKWUMHBQlICdBVZ25.haDkY.dv99sGadvV6Nrx24FP3RdXC3.VQx0p0wK4BdeA; wcs_bt=s_2cb388a4aa34:1656052858; _ga_FW3CMDM313=GS1.1.1656051867.1.1.1656052858.0; _ga=GA1.1.47d4c98e-c974-4a4b-ac53-96a8b5613720; _uetsid=4cc761e0f38611ec8f09d1f0ebbc5bb9; _uetvid=4cc803b0f38611ecb1389123fb6f5977',
                            'currency' : 'TWD',
                            'user-agent':  _useragent
           }
           response =""  
           time.sleep(8)
           resp = requests.get(url, headers=headersItems,  timeout=2400)
           if str(resp.status_code) == '200': 
              response =  resp.text
        except: 
           response =""

        return response


if __name__ == '__main__':
    GetklookSpider(m_id)
    
