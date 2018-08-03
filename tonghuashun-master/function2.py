#-*- coding=utf-8 -*-
import requests
import csv
import pandas as pd

headers={'Accept':'application/json, text/javascript, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection':'keep-alive',
        'Content-Length':'51',
        'Content-Type':'application/x-www-form-urlencoded',
        'DNT':'1',
        'Host':'moni.10jqka.com.cn',
        'Origin':'http://moni.10jqka.com.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}

#请求交易数据,返回JSON格式的交易数据,输入网址,用户ID和用户名称
def requests_transaction_data(UserId,User,url='http://moni.10jqka.com.cn/hezuo/index/searchjyjl/tiaozhan'):
    payload={
        'otherUserId':UserId,
        'otherUser':User,
        'page':'1'}
    r = requests.post(url, data=payload,headers=headers)
    return r.json()


#请求用户数据,返回JSON格式的交易数据,输入网址,用户ID和用户名称
#发现了按照页数请求即可爬到全部的用户数据,没有必要按顺序请求
def requests_user_data(url='http://moni.10jqka.com.cn/hezuo/index/searchph/tiaozhan'):
    payload={
        'page':'1',
        'orderField':'1'}
    r = requests.post(url, data=payload,headers=headers)
    pageCount = r.json()['result']['pages']['pageCount']

    users_list=[]
    for page in range(1,int(pageCount)+1):
        payload={
            'page':str(page),
            'orderField':'1'}
        r = requests.post(url, data=payload,headers=headers)
        for user in r.json()['result']['pmData']:
            L=[user['userName'],user['userid']]
            users_list.append(L)
            write_csv('user_data.csv',L)
        print('第%d页已爬取，总共%d页' %(page,int(pageCount)))
    # return users_list


#输入文件名和列表，执行写入csv操作
def write_csv(file,L):
    with open(file,'a+',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(L)
    csvfile.close()

#读入user_data.csv为dataFrame格式，重命名header并且去重返回
def process_user_data(file_name):
    user_data=pd.read_csv(file_name,encoding='utf8',header=None)
    user_data.rename(columns={0:'user',1:'userid'},inplace=True)
    user_data=user_data.drop_duplicates()
    return user_data


