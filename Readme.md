# Readme
## requirement and install
* elasticsearch - [download](https://www.elastic.co/downloads/elasticsearch)
* java 8 or higher version - [download](https://jdk.java.net/java-se-ri/8-MR3)
* python 3
* python BeautifulSoup package
    * pip install bs4

## config.ini setup
### example
[URL]
boygirl = https://www.ptt.cc/bbs/Boy-Girl/index.html
c_chat = https://www.ptt.cc/bbs/C_Chat/index.html
women = https://www.ptt.cc/bbs/WomenTalk/index.html

[setting]
pages = 50
display_mode = simplify
### detail
在URL欄位中輸入想要爬的PTT看板網址與他的英文看板名稱
在pages欄位裡修改要爬取的頁數
在display_mode欄位中修改想要的顯示模式(simplify/complete), 預設為simplify

## how to use the system
1. 設定 config.ini 裡的參數
2. 執行 PTT_Crawler.py，執行完之後資料夾下會多一個 crawled_data_latest.json檔案
3. 執行 elasticsearch.bat (位在elasticsearch的檔案下)，完成後該cmd畫面不要關掉
4. 執行 import_to_es.py
5. 執行 es_query.py，輸入想搜尋的關鍵字後搜尋結果會依照匹配程度高低顯示，如果要離開系統則輸入 exit
