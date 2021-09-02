#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
個股即時資訊
資料來源
-上市
    https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_1101.tw&json=1&delay=0&_=1582201230288
上櫃
    https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=otc_8069.tw&json=1&delay=0&_=1582201288935

- 取股票名稱
    https://mis.twse.com.tw/stock/api/getStockNames.jsp?n=8069&_=1582201326918

- i.g
-上市
Request
    - http://py.jayi.com.tw:888/rtp01.py?ids=tse_2363
Response
    - 2363!"矽統"!22!22.5500!24.8000!20.3000!24.4000!24.8000!24.0500!24.8!0!24.8!49526!13!14!15!2.25!17!18!9.98!20!21!22!23!4824! 

- 上櫃
    Request
        - http://py.jayi.com.tw:888/rtp01.py?ids=otc_8069
    Response
        - 8069!"元太"!22!55.9000!61.4000!50.4000!56.6000!61.4000!56.6000!61.4!0!61.4!19576!13!14!15!5.5!17!18!9.84!20!21!22!23!4665! 


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
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Import modules for CGI handling 
import cgi, cgitb 
import json
import requests
import json
import numpy
import pandas as pd
#import time
import utility
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
ids = form.getvalue('ids')
if ids is None:
    print ("Content-type:text/html\n")
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
    print ("Content-type:text/html\n")
    #print(query_url)
    #print (df)
    # df.shape  # 得到df的行和列数
    #print (df.shape)
    # df['col1'].count() #去除了NaN的数据
    #print (df['c'].count())
    result = ""
    for index, row in df.iterrows():
        #print(row['c'], row['n'])
        # 記錄實際查到的資料，稍後比對用
        res_ids.append("{ex}_{id}".format(id=row['c'],ex=row['ex']))
        #print(res_ids)
        CurrentPrice = 0
        BuyPrice=0
        SellPrice=0
        BuyV=0
        SellV=0
        if not pd.isnull(row['b']):
            if row['b']=="-": # b 買進5檔 價, if b== "-" => 跌停
                #BuyPrice = 0  # w 跌停價
                CurrentPrice = float(row['w'])
            else:
                BuyPrice = row['b'][0:row['b'].find('_')]
        if not pd.isnull(row['a']):
            if row['a']=="-": # a 賣出5檔 價, if a== "-" => 漲停
                #SellPrice = 0 # u 漲停價
                CurrentPrice = float(row['u'])
            else:
                SellPrice = row['a'][0:row['a'].find('_')]
        if not pd.isnull(row['g']):
            BuyV = row['g'][0:row['g'].find('_')]
        if not pd.isnull(row['f']):
            SellV = row['f'][0:row['f'].find('_')]
        if row['z']!="-":
            CurrentPrice = float(row['z'])
        else:
            CurrentPrice = float(BuyPrice)
        
        if SellPrice==0: # SellPrice==0 代表 漲停，沒有人要賣，此時買價會是漲停價
            BuyPrice = CurrentPrice
        if BuyPrice==0: # v==0 代表 跌停，沒有人要買，此時賣價會是跌停價
            SellPrice = CurrentPrice
        PriceFluctuation = CurrentPrice - float(row['y'])
        PriceFluctuationPercent= '%.2f'%((PriceFluctuation)*100/float(row['y']))
        # '%.2f' % => 除法保留兩位小數點的方法 (ref.https://blog.csdn.net/chenmozhe22/article/details/81666831)
        # print('{code}!"{name}"!22!{y}!{u}!{w}!{open}!{highest}!{lowest}!{BuyPrice}!{SellPrice}!{b}!{v}!13!14!15!{c1}!17!18!{c2}!20!21!22!23!{BuyV}!{SellV}'.format(b=row['z'],code=row['c'], name=row['n'], open=row['o'], highest=row['h'], lowest=row['l'], v=row['v'], y=row['y'], w=row['w'], u=row['u'], c1=PriceFluctuation, c2= PriceFluctuationPercent, SellPrice=SellPrice, BuyPrice=BuyPrice, BuyV=BuyV, SellV=SellV))
        result+='{code}!"{name}"!22!{y}!{u}!{w}!{open}!{highest}!{lowest}!{BuyPrice}!{SellPrice}!{b}!{v}!13!14!15!{c1}!17!18!{c2}!20!21!22!23!{BuyV}!{SellV}\n'.format(b=CurrentPrice,code=row['c'], name=row['n'], open=row['o'], highest=row['h'], lowest=row['l'], v=row['v'], y=row['y'], w=row['w'], u=row['u'], c1=PriceFluctuation, c2= PriceFluctuationPercent, SellPrice=SellPrice, BuyPrice=BuyPrice, BuyV=BuyV, SellV=SellV)
    # 發起 exceptions for Debug
    # raise 
    print(result, end ="") # Print without newline in Python 3.x
    #print(utility.timestamp_milli())
    #print(utility.happy_python())
    #print("<hr>")
    #print(query_url)
    # 比對要查詢的(targets)與實際查到的(res_ids)，如果有缺，補上Error
    diff_ids = list(set(targets) - set(res_ids))
    if len(diff_ids) > 0:
        for id in diff_ids:
            print ("{id}!\"Error\"!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0".format(id=id[id.find('_')+1:]))
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
    jsonData = json.dumps(jsonData)

    print "Content-type: text/json\n\n"
    print jsonData 
    '''

except requests.exceptions.ConnectionError:
    #r.status_code = "Connection refused"
    print ("Content-type:text/html\n")
    for id in targets:
        print ("{id}!\"Error\"!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0".format(id=id[id.find('_')+1:]))

except:
    print ("Content-type:text/html\n")
    for id in targets:
        print ("{id}!\"Error\"!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0!0".format(id=id[id.find('_')+1:]))
