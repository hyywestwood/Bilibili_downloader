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


class football_video_downloader():
    def __init__(self, url, header):
        self.url = url
        self.header = header
        self.title = None
        self.m3u8_name = None # m3u8文件的名称
        self.video_path = None # 用于存放视频的路径
        self.fromer_path = os.path.join(os.getcwd(), 'video') # 视频路径的上一级
        folder = os.path.exists(self.fromer_path)
        if not folder:
            os.mkdir(os.path.join(self.fromer_path))
    
    def run(self):
        self.video_path, self.m3u8_name, self.title = self.get_m3u8(self.url, self.header) # 获取该网址下视频信息，下载对应m3u8文件
        # self.vider_down(self.m3u8_name) # 利用m3u8文件下载，分段的比赛视频，并最终合并呈MP4格式的视频文件
        self.trans_encode() # 不知为何，此时MP4文件虽然能正常播放，但无法拖入剪映，需要再转换一下视频编码


    def get_m3u8(self, url, header):
        response = requests.get(url=url, headers= header)
        html = response.content
        bf = BeautifulSoup(html, 'html.parser')
        temp = bf.find_all('script', type='text/javascript')
        info = str(temp[2].contents[0]).replace('\n','')

        # 获取比赛标题，并生成对应文件夹
        pattern = r'topictitle:".*?"'
        title = re.findall(pattern, info)[0].replace('topictitle:','').replace('"','')
        title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的，预防出现非法字符
        video_path = os.path.join(self.fromer_path, title) # 视频的下载存储位置
        folder = os.path.exists(video_path)
        if not folder:
            os.mkdir(video_path)

        # 使用正则获取m3u8文件地址,下载m3u8文件
        pattern = r'RealtimeUrl: \'.*?\''
        v_url = eval(re.findall(pattern, info)[0].split()[1])
        with closing(requests.get(url=v_url, headers= header, stream=True, timeout=120)) as response:
            chunk_size = 1024 # 单次请求最大值
            with open(os.path.join(video_path, v_url.split('/')[-1]), "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)

        # 获取比赛时间
        pattern = r'tpstarttime: \'.*?\''
        play_time = eval(re.findall(pattern, info)[0].replace('tpstarttime: ',''))

        # 将比赛信息整理，写入json文件保存
        play_info_dict = {
            'video_title': title,
            'play_time': play_time,
            'm3u8_url': v_url,
        }
        with open(os.path.join(video_path, title+'.json'), "w") as f:
            json.dump(play_info_dict,f)

        return video_path, v_url.split('/')[-1], title
    
    # 读取m3u8文件信息,下载ts文件并最后合并为mp4文件
    def vider_down(self, m3u8_name):
        playlist = m3u8.load(os.path.join(self.video_path, m3u8_name))
        
        # 线程池下载ts，引入index可以防止合成时视频发生乱序
        for i in range(2): # 下载两遍，防止部分ts文件因网络原因而未下载
            with ThreadPoolExecutor(max_workers=10) as pool:
                for index, seg in enumerate(playlist.segments):
                    pool.submit(self.save_ts, seg.uri, index, len(playlist.segments))
        
        files = glob.glob(os.path.join(self.video_path, '*.ts'))
        with alive_bar(len(files), title="合成视频", bar="bubbles", spinner="classic") as bar:
            for file in files:
                with open(file, 'rb') as fr, open(os.path.join(self.video_path, self.title + '.mp4'), 'ab') as fw:
                    content = fr.read()
                    fw.write(content)
                os.remove(file)
                bar()
                # time.sleep(0.2)

    def save_ts(self, url, index, total_num):
        filename = os.path.join(self.video_path, str(index).zfill(5) + '.ts')
        if not os.path.exists(filename):
            with closing(requests.get(url=url, headers= header, stream=True, timeout=120)) as response:
                chunk_size = 1024 # 单次请求最大值
                with open(filename, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
            print(filename + ' is ok! ' + '[' + str(index) + '/' + str(total_num)+']')
    
    # 改变视频编码
    def trans_encode(self):
        cmd = 'ffmpeg -i ' + os.path.join(self.video_path, self.title + '.mp4') + \
            ' -vcodec copy -acodec copy -f mp4 ' + os.path.join(self.video_path, self.title + '-2.mp4')
        try:
            # res = subprocess.call(cmd, shell=True)  # "Muxing Done
            subprocess.call(cmd, shell=True)
            # if res != 0:
            #     cmd = 'ffmpeg -i ' + os.path.join(self.video_path, self.title + '.mp4') + \
            #         ' -vcodec copy -an -f mp4 ' + os.path.join(self.video_path, self.title + '-1.mp4')
            #     print('视频转换失败，尝试取消导出音频...')
            #     subprocess.call(cmd, shell=True)  # "Muxing Done
            #     # return False
            # return True
        except Exception:
            print('视频路径有误，请再次尝试...')




if __name__ == '__main__': 
    # url = 'https://wx.vzan.com/live/tvchat-1144900564?shareuid=384105064&vprid=0&sharetstamp=1618714385266' # VS环资
    # url = 'https://wx.vzan.com/live/tvchat-1827957806?v=1621501131000&jumpitd=1#/' # 能源vs公管
    # url = 'https://wx.vzan.com/live/tvchat-1276238835?v=1621504811000&jumpitd=1#/' # 计院vs信电
    # url = 'https://wx.vzan.com/live/tvchat-2003603387?v=1621506997000&jumpitd=1#/' # 控制vs云峰
    # url = 'https://wx.vzan.com/live/tvchat-2124676592?v=1621520152000&jumpitd=1#/' # 建工vs材料
    # url = 'https://wx.vzan.com/live/tvchat-8456138?v=1621743956000&jumpitd=1#/' # 海洋vs建工 
    url = 'https://wx.vzan.com/live/tvchat-1725581328?v=1621743561000&jumpitd=1#/' # 光电vs海洋
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Referer': url,
        } 
    
    foot_d = football_video_downloader(url, header)
    foot_d.run()
    

    
