#-*- coding=utf-8 -*-
from pprint import pprint
from function2 import requests_transaction_data,requests_user_data,process_user_data
import requests




if __name__ == '__main__':

    # requests_user_data()

    for index,row in process_user_data('user_data.csv').head(10).iterrows():
        # print(row['user'],row['userid'])
        pprint(requests_transaction_data(User=row['user'],UserId=row['userid']))
