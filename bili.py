import requests
import json
import os, re
from contextlib import closing
from bs4 import BeautifulSoup
import subprocess


class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


class Bilibili_downloader():
    def __init__(self, url):
        self.url = url
        self.video_path = None
        self.header = {
            # 'Host': 'cn-zjjh4-dx-v-14.bilivideo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Referer': self.url,
            'Origin': 'https://www.bilibili.com',
            'Range': 'bytes=0-' # 该参数设置使视频完整下载
        }
    
    # 获取视频真实下载链接
    def get_real_address(self, url, getHtmlHeaders):
        response = requests.get(url=url, headers= getHtmlHeaders)
        html = response.content
        bf = BeautifulSoup(html, 'html.parser')

        # 确定视频名称，并据此新建文件夹
        self.video_title = bf.find('h1', class_='video-title').attrs['title']
        self.video_title = re.sub(r'[\/\\:*?"<>|]', '', self.video_title)  # 替换为空的
        self.video_path = os.path.join(os.getcwd(), 'video', self.video_title)
        folder = os.path.exists(self.video_path)
        if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
            os.mkdir(self.video_path)
        
        a = bf.find_all('script')
        info = json.loads(str(a[4].contents[0])[20:])
        AudioURl = info['data']['dash']['audio'][0]['baseUrl'] # 视频默认选择最高画质
        VideoURl = info['data']['dash']['video'][0]['baseUrl']
        return AudioURl, VideoURl
    
    def downloader(self, AudioURl, VideoURl):
        # 下载音频
        with closing(requests.get(url=AudioURl, headers= self.header, stream=True)) as response:
            chunk_size = 1024 # 单次请求最大值
            content_size = int(response.headers['content-length']) # 内容体总大小
            progress = ProgressBar(self.video_title + '-音频', total=content_size,
                                            unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
            with open(os.path.join(self.video_path, 'audio.mp4'), "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        
        # 下载视频
        with closing(requests.get(url=VideoURl, headers= self.header, stream=True)) as response:
            chunk_size = 1024 # 单次请求最大值
            content_size = int(response.headers['content-length']) # 内容体总大小
            progress = ProgressBar(self.video_title + '-视频', total=content_size,
                                            unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
            with open(os.path.join(self.video_path, 'video.mp4'), "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
    
    # 将下载下来的音频和视频合并
    def combination(self, outfile_name):
        # os.chdir(os.path.join(os.getcwd(), 'video'))
        # 使用此命令需要提前下载ffmpeg，并将其添加至环境变量
        cmd = 'ffmpeg -i ' + os.path.join(self.video_path, 'audio.mp4') + \
            ' -i ' + os.path.join(self.video_path, 'video.mp4') + ' -strict -2 ' + os.path.join(self.video_path, outfile_name + '.mp4')
        # print(cmd)
        try:
            print('开始视频合成，请耐心等待...')
            # subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)  # "Muxing Done
            subprocess.call(cmd, shell=True)  # "Muxing Done
            print('视频合并完成！')
        except Exception:
            print('视频路径有误，请再次尝试...')
        

    def run(self):
        self.AudiouURL, self.VideoURL = self.get_real_address(self.url, self.header)
        # self.downloader(self.AudiouURL, self.VideoURL)
        self.combination(self.video_title)

if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV17V411E72C'
    dw = Bilibili_downloader(url)
    dw.run()
    # print('水水水水是是是')


