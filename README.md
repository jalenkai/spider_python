# python爬蟲
## 爬蟲常用的套件
from bs4 import BeautifulSoup  *將原始碼轉換lxml結構(結構化)
from selenium import webdriver *是用瀏覽器爬蟲之工具(動態網站技術的利器)
import urllib3 *提供網站get,post方法傳出原始碼(http.request)
import requests *提供網站get,post方法傳出原始碼
import threading *提供多線程方法(執行序)
from multiprocessing import Pool *提供非同步方法
from lxml import etree  *提供xml文件的套件
import json *提供json文件的套件
import datetime,time *提供時間及日期的方法套件
import os *提供系統相關的方法
import pandas as pd *提供python字典物件的方法


## books.py
> 博客來購物網站範例
- 1.非同步執行apply_async或執行緒threads方法
- 2.連結MS-SQL資料庫
- 3.資料分批運作
- 4.商品產生XML檔方法
## klookfor_google_cloud.py
> klook
- 1.google.cloud連結方式
- 2.google bigquery 運用
- 3.商品資訊產生json檔
- 4.dice字典運用
## GetWikiSpider.py
> Wiki
- 1.傳入關鍵字傳出Wiki資訊
- 2.class寫法

## momoshop.py
> momo購物網
>> 先爬商品分類項目,在爬商品內容
- 1.網站內部 api request 爬法
- 2.requests.post 傳值 爬法
- 3.傳出json使用
- 4.正規表示式用法
- 5.匯出xml檔案
- 6.連結ms sql