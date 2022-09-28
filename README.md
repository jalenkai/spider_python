# python爬蟲
## 實務上爬蟲目的
- 將網站的資料來進行分析或運用，而取得的方式除了透過網站所提供的API(Application Programming Interface)外，也可以利用Python來開發爬蟲程式，將網頁的HTML內容下載下來。
- API(Application Programming Interface)：通常網站提供URL傳出JOSN或XML格式，呈現在網站內容上。
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
## HTML原始碼節點認識與搜尋方法
* BeautifulSoup安裝
-- 用來解析HTML結構的套件(Package)，取回的網頁HTML結構，其提供的方法(Method)，輕鬆的搜尋及擷取網頁上所需的資料。
-- 引用requests套件(Package)，透過get()方法，獲取網頁原始碼。

1. 透過pip指令來進行安裝
2. pip install beautifulsoup4
3. pip install requests
 
-- 將網頁的HTML程式碼擷取回來後，並引用BeautifulSoup類別(Class)，傳入取回的HTML結構字串，來解析型態來建物件，如下範例：

```
import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://www.momoshop.com.tw/category/DgrpCategory.jsp?d_code=4300100018&TOP30=Y&sourcePageType=4")
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())  #秀出排版後的HTML程式碼
```

> 擷取部分程式碼：

```
<html lang="zh">
<head>
<link rel="shortcut icon" href="/main/favicon.ico"/>
<link rel="Bookmark" href="/main/favicon.ico"/>
<link rel="icon" href="/main/favicon.ico" type="image/ico"/>
<link rel="search" href="/search/openSearch.xml" type="application/opensearchdescription+xml" title="momo購物網"/>

<link rel="canonical" href="https://www.momoshop.com.tw/category/DgrpCategory.jsp?d_code=4300100018">
<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.momoshop.com.tw/category.momo?top30=y&cn=4300100018">

<title>&#31558;&#38651;&#25490;&#34892;TOP30,&#39208;&#38263;&#25512;&#34214;,&#31558;&#35352;&#22411;&#38651;&#33126;,&#38651;&#33126;/&#32068;&#20214;-momo&#36092;&#29289;&#32178;</title>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="Title" content="&#31558;&#38651;&#25490;&#34892;TOP30,&#39208;&#38263;&#25512;&#34214;,&#31558;&#35352;&#22411;&#38651;&#33126;,&#38651;&#33126;/&#32068;&#20214;-momo&#36092;&#29289;&#32178;">
<meta name="Author" content="momo購物網">
<meta name="Subject" content="momoshop,momo購物網">
.....部分程式碼.....
```

* 以HTML標籤及屬性搜尋節點
** 由soup物件進行節點搜尋
1. find() ：搜尋第一個符合條件的HTML節點

```
result = soup.find("title")
print(result)

```

2. find_all()：搜尋網頁中所有符合條件的HTML節點，如要更明確的搜尋，可以利用關鍵字參數(Keyword Argument)指定其屬性值。若執行結果搜出許多的HTML內容，也可以利用limit關鍵字參數(Keyword Argument)限制搜尋的節點數量，如下範例：(回傳了一個串列(List))

```
result = soup.find_all("p", class="groupName", limit=3)
print(result)

```
```
同時搜尋多個HTML標籤，可以將標籤名稱打包成串列(List)後，傳入find_all()方法(Method)中即可，如下範例：
result = soup.find_all(["h3", "p"], limit=2)
print(result)
```

3. select_one()：當某一節點下只有單個子節點時
```
result = soup.find("h3", itemprop="headline")
print(result.select_one("a"))
```
4. select()：某一節點下有多個子節點時
```
result = soup.find("div", itemprop="itemListElement")
print(result.select("a"))
```

* 以CSS屬性搜尋節點
*  搜尋父節點
*  搜尋前、後節點
*  取得屬性值
*  取得連結文字



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