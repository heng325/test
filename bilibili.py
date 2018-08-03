#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''B站视屏数据爬取 本程序循环爬取了B站编号前一万的视屏及其基本信息，
包括： aid(视频编号)、view(播放量)、danmaku(弹幕数)、reply(评论数)、
favorite(收藏数)、coin(硬币数)、share(分享数) 为了避免被封IP，
每次爬取都有一定的间隔，同时为了加快爬取速度，使用了python多线程技术。
从效果上看，爬取效率还是挺高的。 可以在此基础上对数据进行处理，
包括获取播放量前十的视屏，评论量前十的视频等。 观看视频的链接为
https://www.bilibili.com/video/av + aid。'''

import threading
from collections import namedtuple
from concurrent import futures
import time
import requests
import pymongo

header = ["aid", "view", "danmaku", "reply", "favorite", "coin", "share"]
Video = namedtuple('Video', header)
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
total = 1
result = []
lock = threading.Lock()

def run(url):
    global total
    req = requests.get(url, headers = headers, timeout=6).json()
    time.sleep(0.5)
    try:
        data = req['data']
        video = Video(data['aid'],
                      data['view'],
                      data['danmaku'],
                      data['reply'],
                      data['favorite'],
                      data['coin'],
                      data['share']
                      )
        with lock:
            result.append(video)
            print(total)
            total += 1
    except:
        pass

def save():
    with open("result.csv", "w+") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerow(result)

if __name__ == "__main__":
    urls = ["http://api.bilibili.com/archive_stat/stat?aid={}".format(i)
            for i in range(1000)]
    with futures.ThreadPoolExecutor(32) as executor:
        executor.map(run, urls)
    save()