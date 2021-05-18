from alive_progress.core.progress import alive_bar
import requests
import json
import os, re, time, m3u8
from contextlib import closing
from bs4 import BeautifulSoup
import subprocess
from bili import ProgressBar
from alive_progress import alive_bar



if __name__ == '__main__':
    # 尝试读取m3u8文件
    # pass
    
    # 读取m3u8文件信息
    playlist = m3u8.load(os.path.join(os.getcwd(), 'football', 'replay.1621145343.89870166.m3u8'))
    print(len(playlist.segments))
    # urls = playlist.files
    # play_list = []
    # with open(os.path.join(os.getcwd(), 'football', 'replay.1621145343.89870166.m3u8')) as f:
    #     for line in f:
    #         # print(line)
    #         if line.startswith('#'):
    #             pass
    #         else:
    #             play_list.append(line[:-1])
    # ts_name = play_list[0].split('/')[-1]
    # 下载视频分段ts视频
    # header = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    #         'Accept': '*/*',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #         'Connection': 'keep-alive',
    #         'Referer': 'https://wx.vzan.com/live/tvchat-2028833656?shareuid=384105064&vprid=0&sharetstamp=1621126846232',
    #     } 

    # with alive_bar(len(play_list)) as bar:
    #     for i in range(len(play_list)):
    #         ts_name = play_list[i].split('/')[-1]
    #         ts_path = os.path.join(os.getcwd(), 'football', ts_name)
    #         if not os.path.exists(ts_path):
    #             with closing(requests.get(url=play_list[i], headers= header, stream=True)) as response:
    #                 chunk_size = 1024 # 单次请求最大值
    #                 # content_size = int(response.headers['content-length']) # 内容体总大小
    #                 # progress = ProgressBar(ts_name, total=content_size,
    #                 #                                 unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
    #                 with open(os.path.join(os.path.join(os.getcwd(), 'football', ts_name)), "wb") as file:
    #                     for data in response.iter_content(chunk_size=chunk_size):
    #                         file.write(data)
    #                         # progress.refresh(count=len(data))
    #         bar()
    #         time.sleep(1)

    # 分段视频合并
    # file_name = '海洋-管院.ts'
    # with open(os.path.join(os.getcwd(), 'football', file_name),'wb') as f_out:
    #     for i in range(len(play_list)):
    #         ts_name = play_list[i].split('/')[-1]
    #         f_out.write(open(os.path.join(os.getcwd(), 'football', ts_name),'rb').read())
    # print('finished')
