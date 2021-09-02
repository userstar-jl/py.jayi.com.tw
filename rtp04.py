#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
個股即時資訊

上市: https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_1101.tw&json=1&delay=0&_=1582201230288
上櫃: https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_8069.tw&json=1&delay=0&_=1582201288935

取股票名稱: https://mis.twse.com.tw/stock/api/getStockNames.jsp?n=8069&_=1582201326918
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
from datetime import datetime

# 設定輸出格式
print ("Content-type:application/json;charset=UTF-8")
print ("Access-Control-Allow-Origin:*")
print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出各式

# Create instance of FieldStorage 
form = cgi.FieldStorage() 
# Get data from fields
ids = form.getvalue('ids')
data_date = form.getvalue('data_date')
if ids is None:
    result = {"Success":False,"Msg":"An Error occurred:{}".format("ids is null. 沒有欲查詢的股票代碼"), "timestamp":utility.timestamp_milli()}
    print (jsonData = json.dumps(result))

if data_date is None:
    data_date = utility.getLastTradingDay()
#req_ids= ids.split(",")
res_ids = list() # mis.twse.com.tw 有回覆的股票價格資訊
#print "Content-type:text/html\n"
#print "代碼!股票名稱a!22!33!44!55!66!77!88!99!000!111!222!333"

#targets = ['1101','1102','1103']
targets = ids.split(',')
#stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets) 上市
#stock_list = '|'.join('otc_{}.tw'.format(target) for target in targets) 上櫃
stock_list = '|'.join('{}.tw'.format(target) for target in targets)
stock_list01 = ','.join('{}'.format(target[4:]) for target in targets)
#print "<h2>Hello %s %s</h2>"% (stock_list, stock_list)
try:
    # raise
    result = ""
    sotcksData = []
    stock_price = utility.get_stock_price(data_date, stock_list01)
    if(not stock_price["Result"]):
        result = {"Success":False, "Msg":stock_price["Msg"], "timestamp":utility.timestamp_milli(), "DataDate": data_date, "Data":[]}
    else:
        # sotcksData = stock_price["Data"]
        # 0代號,1名稱,2上市櫃,3成交股數,4成交筆數,5成交金額,6開盤,7最高,8最低,9收盤,10昨日收盤,11漲跌,12漲跌幅,13最後買價,14最後買量,15最後賣價,16最後賣量
        for data in stock_price["Data"]:
            sotcksData.append({
            "code":data[0], 
            "name":data[1], 
            "price":data[9], 
            "o":data[6], 
            "h":data[7], 
            "l":data[8],  
            "v":data[3], 
            "y":data[10], # y 昨收價
            "z":data[9], # z 當盤成交價
            "pfp":data[12]*100}) # 漲跌幅
        # raise 
        # print(result, end ="") # Print without newline in Python 3.x
        #print(utility.timestamp_milli())
        #print(utility.happy_python())
        #print("<hr>")
        #print(query_url)
        # 比對要查詢的(targets)與實際查到的(res_ids)，如果有缺，補上Error
        # diff_ids = list(set(targets) - set(res_ids))
        # if len(diff_ids) > 0:
        #     for id in diff_ids:
        #         sotcksData.append({
        #             "code":id[id.find('_')+1:], 
        #             "name":"--", 
        #             "price":0, 
        #             "o":"--", 
        #             "h":"--", 
        #             "l":"--",  
        #             "v":"--", 
        #             "y":"--", 
        #             "z":"--", 
        #             "pfp":0})
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
        #jsonData = json.dumps(sotcksData)
        result = {"Success":True, "Msg":"", "timestamp":utility.timestamp_milli(), "DataDate": data_date, "Data":sotcksData}
    
    print (json.dumps(result))
except Exception as e:
    sotcksData = []
    for id in targets:
        sotcksData.append({"code":id[id.find('_')+1:], "name":"--", "price":0, "pfp":0})
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    # print(errMsg)

    result = {"Success":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":utility.timestamp_milli(), "DataDate": data_date, "Data":sotcksData}
    print (json.dumps(result))