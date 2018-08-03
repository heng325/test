#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import requests #使用requests包方便
import json #导入json模块
import time #导入时间模块

# 以下是某个新闻网站的行情api，返回json格式数据
data = requests.get("https://forexdata.wallstreetcn.com/real?en_prod_code=XAGUSD,AUTD,XAUUSD,USOIL,US10YEAR,GBPUSD,EURUSD,USDJPY,USDCNH,USDOLLARINDEX,UK100INDEX,FRA40INDEX,GER30INDEX,000001,HKG33INDEX,JPN225INDEX&fields=prod_name,update_time,last_px,px_change,px_change_rate,price_precision")
#解析数据，获取需要的内容
injson = json.loads(data.text)['data']['snapshot']
#自己需要的行情代码列表
codelist = "XAGUSD,AUTD,XAUUSD,USOIL,US10YEAR,GBPUSD,EURUSD,USDJPY,USDCNH,USDOLLARINDEX,UK100INDEX,FRA40INDEX,GER30INDEX,000001,HKG33INDEX,JPN225INDEX"

codelistar = codelist.split(',') #个人需要分割成list格式

codelistar.reverse()#反转顺序
print (" 更新时间              品种列表     涨跌幅度   报价 ") #输出标题
for name in codelistar:
    timestr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(injson[name][1]))
    print (timestr +  '  '+injson[name][0]+'   '+str(injson[name][4])+ '  '+str(injson[name][2]))
#最后输出打印出来