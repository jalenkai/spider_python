
import pandas
import pymssql
import cursor
import os,shutil
import sys
import command as comm

sqlserverIP = '192.168.5.60'
ipaddr = comm.get_ip_address()
UspApiPatch = r"C:\FP_GOODS\Data"
if (ipaddr.find(".60") >0) :
   Dstfilename = r"C:\FP_GOODS\Data"
else:
   Dstfilename = r"E:\Data"

def CommitgoodsTempTable(strSQL):
       try:
           goodsTemp_conn1 = pymssql.connect(server=str(sqlserverIP), user='sa', password='tony', database='apitemptb', timeout=2400, login_timeout=600)
           cursor1 = goodsTemp_conn1.cursor()
           cursor1.execute(strSQL)
           goodsTemp_conn1.commit()
           goodsTemp_conn1.close()
           return 1
       except :
           return 0
           goodsTemp_conn1.close()

if __name__ == '__main__':
   dfs = pandas.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW')
   #取得欄位資料
   currency = dfs[0].ix[:,0:5]
   #定義欄位名稱
   currency.columns = ['Currency','Cashrate_buy','Cashrate_Sell','Spotrate_buy','Spotrate_Sell']
   #抽取幣別英文 字串部分 :利用正規表示式
   currency['Currency'] = currency['Currency'].str.extract('\((\w+)\)')
   #直接存檔蓋過
   comm.chkPatchDelFiles(Dstfilename , "currency.csv") #刪除xml暫存檔
    
   sys.path.append("../")
   currency.to_csv(Dstfilename + r"\currency.csv")
   #if (os.path.exists(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python35\currency.csv')):
   #   shutil.move(r"C:\Users\Administrator\AppData\Local\Programs\Python\Python35\currency.csv", Dstfilename + r"\currency.csv")
   #else :
   #     shutil.move(r"C:\FP_GOODS\python\webspider\webspider\currency.csv", Dstfilename + r"\currency.csv")
   
   #exec SetCSVFile2PrimallTemp 'ExchangeRate','C:\FP_GOODS\Data\currency.csv',''
   if (comm.isfileExists(Dstfilename + r"\currency.csv")):
      try:
          filenameR =  UspApiPatch + str('\currency.csv')
          execSQL = "EXEC SetCSVFile2PrimallTemp '" + str('ExchangeRate')  + "','" + filenameR + "',''"
          CommitgoodsTempTable(execSQL)
          print('彙整完成!!')
      except:
            os.rename(filenameR,filenameR + ".error") 

