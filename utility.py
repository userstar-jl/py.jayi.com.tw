#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import pymysql
import json 
import sys
import traceback
from datetime import datetime
from datetime import timedelta
import calendar
import pandas as pd
from io import StringIO
import os
import telegram

# 資料庫參數設定
db_settings = {
    "host": "192.168.1.13",
    "port": 3306,
    "user": "j20521007",
    "password": "j10551055",
    "db": "stock_sys",  
    "cursorclass": pymysql.cursors.DictCursor,
    "charset": "utf8"
}

def timestamp_milli():
    return str(int(round(time.time() * 1000)))

# 今天是否有交易，如果require_date is None
def getDateOpenOrNot(require_date=None, isMore=False):
    # 今天是否開市 規則：六日不開市 && 特殊節日不開市
    if require_date==None:
        require_date = datetime.today().strftime("%Y%m%d") 
        # datetime.strptime(startDateString, "%Y%m%d")

    open_or_not = False
    resultData = []
    # 是否為特殊節日
    sql_command = "select * from holiday_schedule where holiday_date=%s;"
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 執行指令
            number_of_rows = cursor.execute(sql_command, require_date)
            field_names = [i[0] for i in cursor.description]
            # 取得所有資料
            result_set = cursor.fetchall()
            if number_of_rows!=0:
                result = {"Result":False,"Msg":result_set[0]["holiday_name"], "timestamp":timestamp_milli()}
                # return json.dumps(result)
            else:
                require_date_dt = datetime.strptime(require_date, "%Y%m%d")
                if require_date_dt.weekday() in (5,6):
                    result = {"Result":False,"Msg":calendar.day_name[require_date_dt.weekday()], "timestamp":timestamp_milli()}
                else:
                    result = {"Result":True,"Msg":calendar.day_name[require_date_dt.weekday()], "timestamp":timestamp_milli()}

            # return json.dumps(result)
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        result = {"Result":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":timestamp_milli()}
        # return json.dumps(result)
    # result = {"Result":True ,"Msg":calendar.day_name[require_date_dt.weekday()], "timestamp":timestamp_milli()}
    if isMore:
        return result
    else:
        return result["Result"]

# 現在是否為交易時間
def getNowOpenOrNot():
    if json.loads(getDateOpenOrNot('20210611'))["Result"]:
        return is_time_between("15:00", ("09:00", "13:30"))
    else:
        return False

# is_time_between
def is_time_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def get_stock_price_db(stocks):
    sql_command = "select * from daily_stock_quotes where Code IN (%s);"
    format_strings = ','.join(['%s'] * len(stocks))
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # 執行指令
            number_of_rows = cursor.execute(sql_command % format_strings,
                tuple(stocks))
            field_names = [i[0] for i in cursor.description]
            # 取得所有資料
            result_set = cursor.fetchall()
            if number_of_rows!=0:
                result = {"Result":True,"Msg":result_set, "timestamp":timestamp_milli()}
                # return json.dumps(result)
            else:
                result = {"Result":False,"Msg":sql_command, "timestamp":timestamp_milli()}

            # return json.dumps(result)
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        result = {"Result":False,"Msg":"An Error occurred:{}".format(errMsg), "timestamp":timestamp_milli()}
    return result

def get_stock_price(dataDate, stocks):
    targets = stocks.split(',')
    filePath = "/mnt/yau/stock_sys/data/ExchangeReport/DailyExchangeReport_"+ dataDate +".csv"
    if not os.path.isfile(filePath):
        return {"Result":False,"Msg":"An Error occurred:{}".format("上市櫃資料不存在(" + filePath + ")"), "timestamp":timestamp_milli()}
    file = open(filePath, encoding='utf-8')
    data = file.read()
    file.close()
    srcDf = pd.read_csv(StringIO(data), header=0)
    resultDf = srcDf.loc[srcDf['代號'].isin(targets)]
    return {"Result":True,"Data":resultDf.values.tolist(), "timestamp":timestamp_milli()}
    # return {"Result":True,"Data":resultDf.to_json(orient="values", force_ascii=False), "timestamp":timestamp_milli()}
    # return resultDf.to_json(orient="split", index = False)

def getTradingTimeStatus(require_date=None, require_time=None, writeToDB=False):
    real_time = False
    if require_date==None:
        require_date = datetime.today().strftime("%Y%m%d")
    if require_time==None:
        require_time = datetime.today().strftime("%H%M%S")
    result = ""

    date_open_or_not = getDateOpenOrNot(require_date, isMore=True)
    if(not date_open_or_not["Result"]):
        result = getLastTradingDay(require_date)
    else:
        if(is_time_between(require_time, ("090000", "155000"))):
            result = "RealTime"
            real_time = True
        elif(is_time_between(require_time, ("155001", "235959"))):
            result = require_date
        elif(is_time_between(require_time, ("000000", "085959"))):
            result = getLastTradingDay(require_date)
        else:
            result = "Error"
    if writeToDB:
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            cursor.execute("DELETE From global_variables;")
            sql_command = "INSERT INTO global_variables(DateOpenOrNot, Day, RealTime, StockPriceStatus)VALUES(%s, %s, %s, %s);"
            cursor.execute(
                sql_command, (date_open_or_not["Result"], date_open_or_not["Msg"], real_time, result)
            )
            conn.commit()                
    return {"DateOpenOrNot": date_open_or_not["Result"], "Day": date_open_or_not["Msg"], "RealTime": real_time, "StockPriceStatus": result, "UpdateTime": "{}{}".format(require_date, require_time)}

# def getMarketStatus(require_date=None, require_time=None):
#     if require_date==None:
#         require_date = datetime.today().strftime("%Y%m%d")
#     if require_time==None:
#         require_time = datetime.today().strftime("%H%M")
#     trading_time_status = getTradingTimeStatus(require_date, require_time)
#     date_open_or_not = getDateOpenOrNot(require_date)
#     return {"TreadingTimeStatus": trading_time_status}

# 取得查詢日期的前一個交易日,if requestDateString==None 則取得最近的交易日(包含今天)
def getLastTradingDay(requestDateString=None):
    if(requestDateString==None):
        requestDate = datetime.today()
        index = 0
    else:
        requestDate = datetime.strptime(requestDateString, "%Y%m%d")
        index = 1
    got = False
    while not got:
        tmpDate = (requestDate + timedelta(-index)).strftime("%Y%m%d")
        #檢查是否有開示
        if(getDateOpenOrNot(tmpDate)):
            got = True
            return tmpDate
        index += 1

# 傳送Telegram message
def sendTelegramBot(token = "864704853:AAEkFiw_0lkNAhEf-H-WlpDB4yFk8oojpuc", chat_id = "-320544649", message = "Test"):
    bot = telegram.Bot(token=token)
    # now = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    # data_date = datetime.datetime.today().strftime("%Y%m%d")
    bot.send_message(chat_id=chat_id, text= message, parse_mode=telegram.ParseMode.HTML)

if __name__ == '__main__':
    # print('Call it locally')
    # print(getOpenDateOfToday(10))
    # print(getOpenDateOfBetween('20210410','20210421'))
    # todaydate = datetime.today()
    # print(getDateType(todaydate, 1))

    # date_time_str = '2021-04-23 08:15:27.243860'
    # date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    # print(getDateType(date_time_obj, 1))
    # print(getDateOpenOrNot(require_date='20210614', isMore=True))
    # print(getDateOpenOrNot())
    # print(getTradingTimeType('20210611', '002930'))
    # print(getTradingTimeStatus())
    # getTradingTimeStatus(require_date='20210614',require_time='0910',writeToDB=True)
    # sendTelegramBot(message="QQQ")
    # print(getLastTradingDay('20210615'))
    # print(getNowOpenOrNot())
    # print(get_stock_price('20210611', '1442,2337,8069,2330'))
    print(get_stock_price_db(['2330','2337']))
    print("------")
    print(get_stock_price_db([2330,2337]))
    print("END")