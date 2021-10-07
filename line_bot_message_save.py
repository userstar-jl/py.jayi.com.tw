#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# line_bot_message_save.py

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Import modules for CGI handling 
import cgi, cgitb 
import json
import requests
#import time
import utility

# 設定輸出格式
print ("Content-type:application/json;charset=UTF-8")
print ("Access-Control-Allow-Origin:*")
print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出各式


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
data = form.getvalue('data')
if data is None:
    result = {"Success":False,"Msg":"An Error occurred:{}".format("No data"), "timestamp":utility.timestamp_milli()}
    print (json.dumps(result))
else:
    try:
        # utility.timestamp_milli()
        
        utility.save_line_bot_message(data=data)
        # utility.downlaod_line_bot_file(message=data)

        result = {"Success":True, "Msg":"", "timestamp":utility.timestamp_milli()} 
        print (json.dumps(result))

    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        # print(errMsg)

        result = {"Success":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":utility.timestamp_milli()}
        print (json.dumps(result))
