#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
權股價指數/櫃買指數/寶島股價指數擷取
https://mis.twse.com.tw/stock/data/mis_IDX.txt?_=1582683995922

'''

''' python2 'ascii' codec can't encode characters in ordinal not in range(128) 的解決方法
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 
'''

''' python3 'ascii' codec can't encode characters in ordinal not in range(128)的解決方法
ref. https://blog.csdn.net/TH_NUM/article/details/80685389
'''
import sys
import codecs
# Import modules for CGI handling 
import cgi, cgitb 
import sys, json
import requests
import utility
import traceback
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

try:
    print ("Access-Control-Allow-Origin: *")#跨域請求 泛域名: (* 允許所有域名的指令碼訪問該資源。)

    query_url = "https://mis.twse.com.tw/stock/data/mis_IDX.txt?_=" + utility.timestamp_milli()
    print ("Content-type:text/html\n")
    
    #requests = requests.get(query_url, headers = headers, timeout = 20) 
    requests.adapters.DEFAULT_RETRIES = 1 # 设置重连次数
    res = requests.get(query_url, timeout=3)
    print (res.text)

except requests.exceptions.ConnectionError:
    #r.status_code = "Connection refused"
    print ("Content-type:text/html\n")
    print ("ConnectionError")

except requests.exceptions.ConnectionError:
    print('ConnectionError -- please wait 3 seconds')
    print ("Content-type:text/html\n")
    #time.sleep(3)
except requests.exceptions.ChunkedEncodingError:
    print ("Content-type:text/html\n")
    print('ChunkedEncodingError -- please wait 3 seconds')
    ##Atime.sleep(3)    
    
except Exception as e:
    print ("Content-type:text/html\n")
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)
    
