#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
import json

from urllib.parse import urlencode
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError

def get_page_index(offset, keyword):
    data = {
        'offset': offset ,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        # 'from':'search_tab',
    }
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):

    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        print(url)

if __name__ == '__main__':
    main()