# python爬蟲
## 實務上爬蟲目的
- 將網站的資料來進行分析或運用，而取得的方式除了透過網站所提供的API(Application Programming Interface)外，也可以利用Python來開發爬蟲程式，將網頁的HTML內容下載下來。
- API(Application Programming Interface)：通常網站提供URL傳出JOSN或XML格式，呈現在網站內容上。
## HTML原始碼節點認識與搜尋方法
* BeautifulSoup安裝
** 用來解析HTML結構的套件(Package)，取回的網頁HTML結構，其提供的方法(Method)，輕鬆的搜尋及擷取網頁上所需的資料。
** 引用requests套件(Package)，透過get()方法，獲取網頁原始碼。

1. 透過pip指令來進行安裝
2. pip install beautifulsoup4
3. pip install requests

>> 範例：
```
import requests
response = requests.get(
    "https://www.momoshop.com.tw/category/DgrpCategory.jsp?d_code=4300100018&TOP30=Y&sourcePageType=4")
```

* 以HTML標籤及屬性搜尋節點

* 以CSS屬性搜尋節點
*  搜尋父節點
*  搜尋前、後節點
*  取得屬性值
*  取得連結文字
## 爬蟲常用的套件
* from bs4 import BeautifulSoup  #將原始碼轉換lxml結構(結構化)
* from selenium import webdriver #是用瀏覽器爬蟲之工具(動態網站技術的利器)
* import urllib3 #提供網站get,post方法傳出原始碼(http.request)爬蟲利器)
* import requests #提供網站get,post方法傳出原始碼(爬蟲利器)
* import threading #提供多線程方法(執行序)技術的套件
* from multiprocessing import Pool #提供非同步技術的套件
* from lxml import etree  #提供xml文件的套件
* import json #提供json文件的套件
* import datetime,time #提供時間及日期的方法套件
* import os #提供系統相關的套件
* import pandas as pd #提供python字典物件的套件
* import math #提供常用數學函數的套件
* import csv #提供csv文件檔的套件
* import logging #提供訊息紀錄方法套件(log檔)

## books.py
> 博客來購物網站範例
1. 非同步執行apply_async或執行緒threads方法
2. 連結MS-SQL資料庫
3. 資料分批運作
4. 商品產生XML檔方法
## klookfor_google_cloud.py
> klook
1. google.cloud連結方式
2. google bigquery 運用
3. 商品資訊產生json檔
4. dice字典運用
## GetWikiSpider.py
> Wiki
1. 傳入關鍵字傳出Wiki資訊
2. class寫法

## momoshop.py
> momo購物網
* 先爬商品分類項目,在爬商品內容
1. 網站內部 api request 爬法
2. requests.post 傳值 爬法
3. 傳出json使用
4. 正規表示式用法
5. 匯出xml檔案
6. 連結ms sql