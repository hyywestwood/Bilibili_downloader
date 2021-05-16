from selenium import webdriver
import requests
import re
import json
from contextlib import closing
from pyquery import PyQuery as pq
from requests import RequestException
from bs4 import BeautifulSoup


if __name__ == '__main__':
    import os
    url = 'https://www.bilibili.com/video/BV1Up4y1472Z?spm_id_from=333.851.b_7265636f6d6d656e64.1'

    # 使用selenium获取视频连接
    # profile = webdriver.FirefoxOptions()
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    # profile.set_preference('general.useragent.override', user_agent)
    # driver = webdriver.Firefox(options=profile)
    # driver.get(url)
    # bf = BeautifulSoup(driver.page_source, 'html.parser')
    # print('aasa')
    # a = bf.find_all('script',text = 'window')
    # a = bf.find_all('script')
    # info = json.loads(str(a[4].contents[0])[20:])
    # info_data = info['data']
    # video_info = info_data['dash']['video']
    # video_16 = video_info[7]
    # video_16['baseUrl']

    # 使用request获取视频连接
    getHtmlHeaders={
            # 'Host': 'cn-zjjh4-dx-v-14.bilivideo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Referer': url,
            'Origin': 'https://www.bilibili.com',
            'Range': 'bytes=0-'
        }
    response = requests.get(url=url, headers= getHtmlHeaders)
    html = response.content
    bf = BeautifulSoup(html, 'html.parser')
    video_title = bf.find('h1', class_='video-title').attrs['title']
    print('sssss')
    # a = bf.find_all('script')
    # info = json.loads(str(a[4].contents[0])[20:])
    # AudioURl = info['data']['dash']['audio'][0]['baseUrl']

    # accept_qulity = [112, 80, 64, 32, 16]
    # accept_description = ['高清 1080P+', '高清 1080P', '高清 720P', '清晰 480P', '流畅 360P']
    # video_info = info['data']['dash']['video']
    
    # # 找出视频可选择的清晰度
    # available_qulity = []
    # for item in video_info:
    #     if item['id'] not in available_qulity:
    #         available_qulity.append(item['id'])

    # print('请选择您想下载的清晰度（输入对应数字）：')
    # for i in range(len(available_qulity)):
    #     print(str(i+1) + ':' + accept_description[accept_qulity.index(available_qulity[i])])
    # choosen = int(input())
    # VideoURL = video_info[choosen]['baseUrl']
    # print(VideoURL)