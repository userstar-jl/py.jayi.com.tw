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
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
ids = form.getvalue('ids')
if ids is None:
    print ("Content-type:text/json\n")
    print ("Access-Control-Allow-Origin:*")
    print ("ids is null. 沒有欲查詢的股票代碼")
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
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list+ "&json=1&delay=0&_=" + utility.timestamp_milli()
    
    requests.adapters.DEFAULT_RETRIES = 1 # 设置重连次数
    res = requests.get(query_url, timeout=3)
    data = json.loads(res.text)
    columns = ['c','n','z','tv','v','o','h','l','y','w', 'u', 'b', 'a','f', 'g', 'ex']
    '''
    c 股票代號, n 公司簡稱, z 當盤成交價, tv 當盤成交量, v 累積成交量, o 開盤價, h 最高價, l 最低價, y 昨收價
    b 買進5檔 價, a 賣出5檔 價, w 跌停價, u 漲停價, f 賣出5檔 量,g 買進5檔 量
    ex: tse or otc
    '''
    df = pd.DataFrame(data['msgArray'], columns=columns)
    # print ("Content-type:text/html\n")
    #print(query_url)
    #print (df)
    # df.shape  # 得到df的行和列数
    #print (df.shape)
    # df['col1'].count() #去除了NaN的数据
    #print (df['c'].count())
    result = ""
    sotcksData = []
    # sotcksData = json.loads(sotcksData)
    for index, row in df.iterrows():
        #print(row['c'], row['n'])
        # 記錄實際查到的資料，稍後比對用
        res_ids.append("{ex}_{id}".format(id=row['c'],ex=row['ex']))
        #print(res_ids)
        BuyPrice=0
        SellPrice=0
        BuyV=0
        SellV=0
        if not pd.isnull(row['b']):
            if row['b']=="-":
                BuyPrice = 0
            else:
                BuyPrice = row['b'][0:row['b'].find('_')]
        if not pd.isnull(row['a']):
            if row['a']=="-":
                SellPrice = 0
            else:
                SellPrice = row['a'][0:row['a'].find('_')]
        if not pd.isnull(row['g']):
            BuyV = row['g'][0:row['g'].find('_')]
        if not pd.isnull(row['f']):
            SellV = row['f'][0:row['f'].find('_')]
        CurrentPrice = 0
        if row['z']!="-":
            CurrentPrice = float(row['z'])
        else:
            CurrentPrice = float(BuyPrice)

        if SellPrice==0:
            SellPrice = CurrentPrice
        if BuyPrice==0:
            BuyPrice = CurrentPrice
            
        PriceFluctuation = CurrentPrice - float(row['y'])
        PriceFluctuationPercent= '%.2f'%((PriceFluctuation)*100/float(row['y']))
        # '%.2f' % => 除法保留兩位小數點的方法 (ref.https://blog.csdn.net/chenmozhe22/article/details/81666831)
        # print('{code}!"{name}"!22!{y}!{u}!{w}!{open}!{highest}!{lowest}!{BuyPrice}!{SellPrice}!{b}!{v}!13!14!15!{c1}!17!18!{c2}!20!21!22!23!{BuyV}!{SellV}'.format(b=row['z'],code=row['c'], name=row['n'], open=row['o'], highest=row['h'], lowest=row['l'], v=row['v'], y=row['y'], w=row['w'], u=row['u'], c1=PriceFluctuation, c2= PriceFluctuationPercent, SellPrice=SellPrice, BuyPrice=BuyPrice, BuyV=BuyV, SellV=SellV))
        result+='{code}!"{name}"!22!{y}!{u}!{w}!{open}!{highest}!{lowest}!{BuyPrice}!{SellPrice}!{b}!{v}!13!14!15!{c1}!17!18!{c2}!20!21!22!23!{BuyV}!{SellV}\n'.format(b=CurrentPrice,code=row['c'], name=row['n'], open=row['o'], highest=row['h'], lowest=row['l'], v=row['v'], y=row['y'], w=row['w'], u=row['u'], c1=PriceFluctuation, c2= PriceFluctuationPercent, SellPrice=SellPrice, BuyPrice=BuyPrice, BuyV=BuyV, SellV=SellV)
        sotcksData.append({
            "code":row['c'], 
            "name":row['n'], 
            "price":CurrentPrice, 
            "o":row['o'], 
            "h":row['h'], 
            "l":row['l'], 
            "v":row['v'], 
            "y":row['y'], 
            "z":row['z'], 
            "pfp":PriceFluctuationPercent})
    # 發起 exceptions for Debug
    # raise 
    # print(result, end ="") # Print without newline in Python 3.x
    #print(utility.timestamp_milli())
    #print(utility.happy_python())
    #print("<hr>")
    #print(query_url)
    # 比對要查詢的(targets)與實際查到的(res_ids)，如果有缺，補上Error
    diff_ids = list(set(targets) - set(res_ids))
    if len(diff_ids) > 0:
        for id in diff_ids:
            sotcksData.append({
                "code":id[id.find('_')+1:], 
                "name":"--", 
                "price":0, 
                "o":"--", 
                "h":"--", 
                "l":"--",  
                "v":"--", 
                "y":"--", 
                "z":"--", 
                "pfp":0})
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
    result = {"Success":True,"Msg":"", "timestamp":utility.timestamp_milli(), "Data":sotcksData}
    jsonData = json.dumps(result)
    print ("Content-type:text/json")
    print ("Access-Control-Allow-Origin: *")
    print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出各式
    print (jsonData)
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

    result = {"Success":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":utility.timestamp_milli(), "Data":sotcksData, "query_url":query_url}
    jsonData = json.dumps(result)
    print ("Content-type:text/json")
    print ("Access-Control-Allow-Origin: *")
    print ("") # 要 Access-Control-Allow-Origin: * 一定要這樣的輸出格式、順序
    print (jsonData)