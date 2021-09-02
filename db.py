#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

'''
import sys
import codecs
#import cgitb
#cgitb.enable()

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Import modules for CGI handling 
import logging
import cgi, cgitb 
import json
import requests
import json 
import numpy
import pandas as pd
#import time
import utility
import traceback
import pymysql
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
ids = form.getvalue('ids')
'''
if ids is None:
    print ("Content-type:text/json\n")
    print ("Access-Control-Allow-Origin:*")
    print ("ids is null. 沒有欲查詢的股票代碼")
'''
#req_ids= ids.split(",")
res_ids = list() # mis.twse.com.tw 有回覆的股票價格資訊
#print "Content-type:text/html\n"
#print "代碼!股票名稱a!22!33!44!55!66!77!88!99!000!111!222!333"

#targets = ['1101','1102','1103']
targets = ids.split(',')
#stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets) 上市
#stock_list = '|'.join('otc_{}.tw'.format(target) for target in targets) 上櫃
stock_list = '|'.join('{}.tw'.format(target) for target in targets)
#print "<h2>Hello %s %s</h2>"% (stock_list, stock_list)
'''

'''
# ts = datetime.datetime.now().timestamp()
#current_milli_time = lambda: int(round(time.time() * 1000))
try:
    # 資料庫參數設定
    db_settings = {
        "host": "192.168.1.13",
        "port": 3306,
        "user": "j20521007",
        "password": "j10551055",
        "db": "stock_sys",
        "charset": "utf8"
    }
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 查詢資料SQL語法
        command = "SELECT * FROM stock_group"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
    '''
    print("<hr>")
    print(targets)
    print("<hr>")
    print(res_ids)
    print("<hr>")
    print(diff_ids)
    print("<hr>")
    '''

    '''
    # json Test
    jsonData = {"success": "true"}
    '''
    #jsonData = json.dumps(resultData)
    resultData = []
    resultData.append({"code":"999", "name":"--", "price":0, "pfp":0})
    # result = {"Success":True,"Msg":"", "timestamp":utility.timestamp_milli(), "Data":resultData}
    jsonData = json.dumps(result)
    print ("Content-type:application/json;charset=UTF-8")
    print ("Access-Control-Allow-Origin: *")
    print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出各式
    print (jsonData)
except Exception as e:
    resultData = []
    resultData.append({"code":"999", "name":"--", "price":0, "pfp":0})
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    # print(errMsg)

    result = {"Success":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":utility.timestamp_milli()}
    jsonData = json.dumps(result)
    print ("Content-type:application/json;charset=UTF-8")
    print ("Access-Control-Allow-Origin: *")
    print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出格式、順序
    print (jsonData)