#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import utility
import traceback
from datetime import datetime

# 設定輸出格式
print ("Content-type:application/json;charset=UTF-8")
print ("Access-Control-Allow-Origin:*")
print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出各式

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
ids = form.getvalue('ids')
require_date = form.getvalue('d')
require_time = form.getvalue('t')
# if ids is None:
#     result = {"Success":False,"Msg":"An Error occurred:{}".format("ids is null. 沒有欲查詢的股票代碼"), "timestamp":utility.timestamp_milli()} 
#     print (json.dumps(result))
#     sys.stdout.close()
#     sys.stderr.close()

if require_date==None:
    require_date = datetime.today().strftime("%Y%m%d")
if require_time==None:
    require_time = datetime.today().strftime("%H%M")

try:
    treading_time_status = utility.getTradingTimeStatus(require_date, require_time)
    result = {"Success":True, "Msg":"", "timestamp":utility.timestamp_milli(), "MarketStatus": treading_time_status}
    # result = {"Success":True}
    print (json.dumps(result))
except Exception as e:
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    # print(errMsg)

    result = {"Success":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":utility.timestamp_milli(), "DataDate": data_date} 
    print (json.dumps(result))