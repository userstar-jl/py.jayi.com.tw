
代號,名稱,上市櫃,成交股數,成交筆數,成交金額,開盤,最高,最低,收盤,昨日收盤,漲跌,漲跌幅,最後買價,最後買量,最後賣價,最後賣量




"Security Code","Trade Volume","Transaction","Trade Value","Opening Price","Highest Price","Lowest Price","Closing Price","Dir(+/-)","Change","Last Best Bid Price","Last Best Bid Volume","Last Best Ask Price","Last Best Ask Volume","Price-Earning ratio",
"2330","28,624,508","25,816","17,401,326,587","608.00","608.00","605.00","605.00","-","4.00","605.00","282","606.00","124","29.02",


# stock_sys/data/ExchangeReport/DailyExchangeReport_20210827.csv
代號	名稱	上市櫃	成交股數	成交筆數	成交金額	開盤	最高	最低	收盤	昨日收盤	漲跌	漲跌幅	最後買價	最後買量	最後賣價	最後賣量									
Code	Name	TSE/OTC	Trade Volume	Transaction	Trade Value	Opening Price	Highest Price	Lowest Price	Closing Price	Yestoday Closing Price	Change	Change person	Last Best Bid Price	Last Best Bid Volume	Last Best Ask Price	Last Best Ask Volume	


# python_web@10.8.1.1/rtp03.py
https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_1215.tw|otc_8069.tw&json=1&delay=0&_=1582201288935

{"msgArray":[{"tv":"-","ps":"-","pz":"-","bp":"0","a":"79.4000_79.5000_79.6000_79.7000_79.8000_","b":"79.3000_79.2000_79.1000_79.0000_78.9000_","c":"1215","d":"20210830","ch":"1215.tw","tlong":"1630294171000","f":"47_33_49_26_37_","ip":"0","g":"13_39_41_31_12_","mt":"032924","h":"79.5000","i":"02","it":"12","l":"79.2000","n":"卜蜂","o":"79.5000","p":"0","ex":"tse","s":"-","t":"11:29:31","u":"87.0000","v":"227","w":"71.2000","nf":"台灣卜蜂企業股份有限公司","y":"79.1000","z":"-","ts":"0"},{"tv":"-","ps":"-","pz":"-","bp":"0","a":"80.7000_80.8000_80.9000_81.0000_81.1000_","b":"80.6000_80.5000_80.4000_80.3000_80.2000_","c":"8069","d":"20210830","ch":"8069.tw","tlong":"1630294178000","f":"32_16_24_53_47_","ip":"0","g":"24_249_68_124_176_","mt":"057943","h":"82.8000","i":"26","it":"12","l":"80.5000","n":"元太","o":"82.0000","p":"0","ex":"otc","s":"-","t":"11:29:38","u":"90.6000","v":"7764","w":"74.2000","nf":"元太科技工業股份有限公司","y":"82.4000","z":"-","ts":"0"}],"referer":"","userDelay":5000,"rtcode":"0000","queryTime":{"sysDate":"20210830","stockInfoItem":2326,"stockInfo":1746144,"sessionStr":"UserSession","sysTime":"11:29:48","showChart":false,"sessionFromTime":-1,"sessionLatestTime":-1},"rtmessage":"OK"}


c 股票代號, n 公司簡稱, z 當盤成交價, tv 當盤成交量, v 累積成交量, o 開盤價, h 最高價, l 最低價, y 昨收價
    b 買進5檔 價, a 賣出5檔 價, w 跌停價, u 漲停價, f 賣出5檔 量,g 買進5檔 
