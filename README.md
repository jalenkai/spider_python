# python爬蟲
##
## 實務上爬蟲目的
- 將網站的資料來進行分析或運用，而取得的方式除了透過網站所提供的API(Application Programming Interface)外，也可以利用Python來開發爬蟲程式，將網頁的HTML內容下載下來。
- API(Application Programming Interface)：通常網站提供URL傳出JOSN或XML格式，呈現在網站內容上。
## 傻瓜級的scrapy爬蟲工具
- 安裝套件：import scrapy or pip install scrapy
- from bs4 import BeautifulSoup
  * 測試一個py
  1. 將在項目的spiders目錄下新建立一個新的 scrapySpider.py
  2. cmd
  3. 執行 scrapy  runspider C:\[py路徑]\scrapySpider.py
- 常用語法：
  * allow=() 正規表示式，提取符合正規的連結
  * deny=() 正则表达式，拒绝符合正規的連結
  * allow_domains() 允許的域名
  * deny_domains=() 拒絕的域名
  * restrict_xpaths=() 提取符合xpath規則的連結
  * restract_css=() 提取符合css規則的連結 
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
- 用來解析HTML結構的套件(Package)，取回的網頁HTML結構，其提供的方法(Method)，輕鬆的搜尋及擷取網頁上所需的資料。
- 引用requests套件(Package)，透過get()方法，獲取網頁原始碼。

1. 透過pip指令來進行安裝
2. pip install beautifulsoup4
3. pip install requests
 
- 將網頁的HTML程式碼擷取回來後，並引用BeautifulSoup類別(Class)，傳入取回的HTML結構字串，來解析型態來建物件，如下範例：

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

> 以HTML標籤及屬性搜尋節點
* 以下皆使用BeautifulSoup套件(Package)方法
* 由soup物件進行節點搜尋
1. find() ：搜尋第一個符合條件的HTML節點

```
result = soup.find("title")
print(result)

```

2. find_all()：搜尋網頁中所有符合條件的HTML節點，如要更明確的搜尋，可以利用關鍵字參數(Keyword Argument)指定其屬性值。若執行結果搜出許多的HTML內容，也可以利用limit關鍵字參數(Keyword Argument)限制搜尋的節點數量，如下範例：(回傳了一個串列(List))

```
result = soup.find_all("p", class_="groupName", limit=3)
print(result)

```
```
同時搜尋多個HTML標籤，可以將標籤名稱打包成串列(List)後，傳入find_all()方法(Method)中即可，如下範例：
result = soup.find_all(["h3", "p"], limit=2)
print(result)
```

3. select_one()：當某一節點下只有單個子節點時
```
result = soup.find("h3", class_="headline")
print(result.select_one("a"))
```
4. select()：某一節點下有多個子節點時
```
result = soup.find("div", class_="itemListElement")
print(result.select("a"))
```

* 以CSS屬性搜尋節點
1. 依據HTML的css屬性來進行節點的搜尋
2. 使用 class 中的關鍵字參數(Keyword Argument)來進行css屬性值的指定
3. find()：搜尋第一個符合指定的HTML標籤及css屬性值的節點
   ```
   titles = soup.find("p", class_="abc")
   print(titles)
   ```
4. find_all()：搜尋網頁中符合指定的HTML標籤及css屬性值的所有節點
   ```
   titles = soup.find_all("p", class_="abc", limit=3)
   print(titles)
   ```
5. select()：透過css屬性值來進行HTML節點的搜尋
   ```
   titles = soup.select(".abc", limit=3)
   print(titles)
   ```
   
*  搜尋父節點
1. 從某一個節點向上搜尋，可以使用BeautifulSoup套件(Package)的find_parent()或find_parents()方法(Method)，如下範例：
```
result = soup.find("a", class_="product_title")
parents_soup = result.find_parents("a")
print(parents_soup)
``` 
*  搜尋前、後節點
1. 在同一層級的節點，想要搜尋前一個節點，可以使用BeautifulSoup套件(Package)的find_previous_siblings()方法，如下範例：
```
result = soup.find("a", class_="product_title")
previous_soup = result.find_previous_siblings("a")
print(previous_soup)
```
2. 相反的，在同一層級的節點，想要搜尋後一個節點，則使用find_next_siblings()方法(Method)，如下範例：
```
result = soup.find("a", class_="product_title")
next_soup = result.find_next_siblings("p")
print(next_soup)
```
*  取得屬性值
1. 利用find_all()方法搜尋網頁中所有<li>標籤且itemprop屬性值為headline的節點，在透過for迴圈讀取串列(List)中的節點，由於之標籤底下只有一個<a>標籤，就可以利用BeautifulSoup套件的select_one()方法進行選取，如下範例：
```
titles = soup.find_all("div", class_="product_image")
for title in titles:
    print(title.select_one("a"))
```
*  取得節點文字或內容
1. 要取得之標籤的連結文字或內容，可以利用BeautifulSoup套件(Package)的getText()方法(Method)，如下範例：
```
titles = soup.find_all("li", class_="product_image")
for title in titles:
    print(title.select_one("img").getText())
```
2. 由於class為Python保留字，所以我們在這裡要使用「class_」來表示。

## books.py
> 博客來購物網站範例
1. 非同步執行apply_async或執行緒threads方法
2. 連結MS-SQL資料庫
3. 資料分批運作
4. 商品產生XML檔方法
## klook for_google_cloud.py
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