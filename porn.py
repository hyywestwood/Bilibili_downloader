from alive_progress.core.progress import alive_bar
import requests
import json
import os, re, time, m3u8
from contextlib import closing
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import glob
from concurrent.futures import ThreadPoolExecutor
import subprocess
from Crypto.Cipher import AES


class porn_downloader():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        }
        self.base_dir = os.path.join(os.getcwd(), 'video', 'porn') # 视频路径的上一级
        self.make_dir(self.base_dir)

        if os.path.exists(os.path.join(self.base_dir, 'video_data_json.json')):
            self.video_data_json = json.load(os.path.join(self.base_dir, 'video_data_json.json'))
        else:
            self.video_data_json = {}

    def run(self):
        self.real_base_url = self.get_real_base_url()
        v_id_list, v_title_list, img_url_list = self.get_video_info(1)
        self.download(v_id_list, v_title_list, img_url_list)
        with open(os.path.join(self.base_dir, 'video_data_json.json'), 'w', encoding='utf-8') as write_f:
	        json.dump(self.video_data_json, write_f, indent=4, ensure_ascii=False)

    # 获取视频真实服务器地址
    def get_real_base_url(self):
        # 观看地址为：ncfhjj.net，但为避免被ban，该网站实际视频请求地址经过了多重重定向
        base_url = 'http://ncfhjj.net/common.js'  
        sess = requests.Session()
        res = sess.get(url=base_url, headers = self.header)
        temp_url = re.search('src=(.*?)>', res.text).group(1) # 获得第一次重定向的网址
        res1 = sess.get(url=temp_url, headers=self.header)
        temp_url_1 = re.search('"0;url=(.*?)"', res1.text).group(1)
        real_url = sess.get(url=temp_url_1, headers=self.header).url.replace('/home.html', '') # 第二次重定向，获得真实的视频地址
        return real_url
    
    def get_video_info(self, page_index):
        video_chinese_url = self.real_base_url + '/video/video_list.html?video_type=2&page_index=' + str(page_index)  # video_type=2: 中文字幕
        res = requests.get(url=video_chinese_url, headers=self.header)

        v_id_list = re.findall('video_id=(\d*)', res.text)
        # v_url_list = re.findall('href="(/video/video_info.*?)"', res.text) # 不再需要此信息，因为视频播放地址可通过v_id直接构造
        v_title_list = re.findall('"movie_name">(.*?)<', res.text)
        for i in range(len(v_title_list)):
            v_title_list[i] = re.sub(r'[\/\\:*?"<>|]', '', v_title_list[i])  # 去除标题中可能存在的非法字符
            v_title_list[i] = re.sub(r' ', '', v_title_list[i])  # 去除标题中可能存在的非法字符
        img_url_list = re.findall('img src="(.*?)"', res.text)
        assert len(v_id_list) == len(v_title_list) == len(img_url_list)
        return v_id_list, v_title_list, img_url_list

    def download(self, v_id_list, v_title_list, img_url_list):
        for i in range(len(v_id_list)):
            if v_id_list[i] not in self.video_data_json:
                video_path = os.path.join(self.base_dir, v_id_list[i]+v_title_list[i])
                self.make_dir(video_path)
                try:
                    self.download_img(img_url_list[i], video_path)
                    self.download_video(v_id_list[i], video_path)
                except:
                    self.real_base_url = self.get_real_base_url()
                    self.download_img(img_url_list[i], video_path)
                    self.download_video(v_id_list[i], video_path)
                self.video_data_json[v_id_list[i]] = {
                    'title': v_title_list[i],
                    'temp_poster_url': img_url_list[i],
                }
                # time.sleep(10)

    def download_video(self, video_id, video_path):
        single_v_url = self.real_base_url + '/video/video_play.html?video_id=' + video_id # 构造视频播放地址
        res = requests.get(url=single_v_url, headers = self.header)
        m3u8_url = re.search('vPlayerM3u8Url = "(.*?)"', res.text).group(1)  # 获取视频m3u8文件地址
        with closing(requests.get(url=m3u8_url, headers= self.header, stream=True, timeout=120)) as response:
            chunk_size = 1024 # 单次请求最大值
            with open(os.path.join(video_path, 'index.m3u8'), "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
        print(os.path.join(video_path, '  index.m3u8') + '  下载完成')

        # 下面利用m3u8文件，下载分段视频，并最终合并
        # pass

    def download_img(self, img_url, video_path):
        with closing(requests.get(url=img_url, headers= self.header, stream=True, timeout=120)) as response:
            chunk_size = 1024 # 单次请求最大值
            with open(os.path.join(video_path, 'poster.jpg'), "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
        print(os.path.join(video_path, '  poster.jpg') + '  下载完成')

    # 生成文件夹
    def make_dir(self, file_path):
        folder = os.path.exists(file_path)
        if not folder:
            os.mkdir(file_path)


if __name__ == '__main__': 
    d = porn_downloader()
    d.run()
    temp = {}

    # base_dir = './video/test_pron'
    # base_header = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    #     } 
    
    # # 观看地址为：ncfhjj.net，但为避免被ban，该网站实际视频请求地址经过了多重重定向
    # base_url = 'http://ncfhjj.net/common.js'  
    # sess = requests.Session()
    # res = sess.get(url=base_url, headers = base_header)
    # temp_url = re.search('src=(.*?)>', res.text).group(1) # 获得第一次重定向的网址
    # res1 = sess.get(url=temp_url, headers=base_header)
    # temp_url_1 = re.search('"0;url=(.*?)"', res1.text).group(1)
    # real_url = sess.get(url=temp_url_1, headers=base_header).url.replace('/home.html', '') # 第二次重定向，获得真实的视频地址

    # video_chinese_url = real_url + '/video/video_list.html?video_type=2&page_index=1'  # 中文字幕
    # # res = sess.get(url=video_chinese_url, headers=base_header)
    # res = requests.get(url=video_chinese_url, headers=base_header)
    # # bf = BeautifulSoup(res.text, 'html.parser')
    # # v_list = bf.find('div', class_='box movie_list')
    # # aa = v_list.find_all('li')
    # # temp = aa[0]
    # # temp.find['a']
    # # print('sssss')
    # v_id_list = re.findall('video_id=(\d*)', res.text)
    # v_url_list = re.findall('href="(/video/video_info.*?)"', res.text)
    # v_title_list = re.findall('"movie_name">(.*?)<', res.text)
    # for i in range(len(v_title_list)):
    #     v_title_list[i] = re.sub(r'[\/\\:*?"<>|]', '', v_title_list[i])  # 去除标题中可能存在的非法字符
    # img_url_list = re.findall('img src="(.*?)"', res.text)
    # assert len(v_id_list) == len(v_url_list) == len(v_title_list) == len(img_url_list)

    # single_v_url = real_url + '/video/video_play.html?video_id=' + v_id_list[0]
    # # res = sess.get(url=single_v_url)
    # res = requests.get(url=single_v_url)
    # m3u8_url = re.search('vPlayerM3u8Url = "(.*?)"', res.text).group(1)


    # vPlayerM3u8Url = "https://vod.hjbfq.com/20210517/Rcm0TJmm/index.m3u8"
    # v_url = 'https://vod.hjbfq.com/20210517/R5nTbnVh/1000kb/hls/index.m3u8'
    # with closing(requests.get(url=v_url, headers= header, stream=True, timeout=120)) as response:
    #     chunk_size = 1024 # 单次请求最大值
    #     with open(os.path.join(base_dir,v_url.split('/')[-1]), "wb") as file:
    #         for data in response.iter_content(chunk_size=chunk_size):
    #             file.write(data)
    
    # playlist = m3u8.load(os.path.join(base_dir, 'index.m3u8'))
    # video_key_url = playlist.keys[0].absolute_uri
    # video_key = requests.get(url=video_key_url, headers=header).text
    
    # for index, seg in enumerate(playlist.segments):
    #     filename = os.path.join(base_dir,str(index).zfill(5) + '.ts')
    #     if not os.path.exists(filename):
    #         with closing(requests.get(url=seg.uri, headers= header, stream=True, timeout=120)) as response:
    #             chunk_size = 1024 # 单次请求最大值
    #             cryptor = AES.new(video_key.encode('utf-8'), AES.MODE_CBC)
    #             with open(filename, "wb") as file:
    #                 for data in response.iter_content(chunk_size=chunk_size):
    #                     file.write(cryptor.decrypt(data))
    #                     # file.write(data)
    #         print(filename + ' is ok! ' + '[' + str(index) + '/' + str(len(playlist.segments))+']')
        # input()
        # pool.submit(self.save_ts, seg.uri, index, len(playlist.segments))
    # files = glob.glob(os.path.join(base_dir, '*.ts'))
    # with alive_bar(len(files), title="合成视频", bar="bubbles", spinner="classic") as bar:
    #     for index in range(len(files)):
    #         with open(os.path.join(base_dir, str(index).zfill(5) + '.ts'), 'rb') as fr, \
    #         open(os.path.join(base_dir, 'tets1' + '.ts'), 'ab') as fw:
    #             content = fr.read()
    #             fw.write(content)
    #         # os.remove(file)
    #         bar()
    # print('hello')

    # json 数据格式保存已下载信息
    # video_data_json = {}
    # video_data_json['66667'] = {
    #     'title': '标题',
    #     'time': '2021-05-28',
    #     'temp_video_url': 'http://github.com/hyywestwood',
    #     'temp_poster_url': 'http://github.com/hyywestwood/poster',
    # }
    # temp_single_json = {
    #     '66666' : {
    #         'title': '标题',
    #         'time': '2021-05-28',
    #         'temp_video_url': 'http://github.com/hyywestwood',
    #         'temp_poster_url': 'http://github.com/hyywestwood/poster',
    #     }
    # }
    # with open("format_json.json", 'w', encoding='utf-8') as write_f:
	#     json.dump(video_data_json, write_f, indent=4, ensure_ascii=False)
    

    
