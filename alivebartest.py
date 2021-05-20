from alive_progress.core.progress import alive_bar
from concurrent.futures import ThreadPoolExecutor
import time
import glob, os

def save_ts(num, index):
    pass
    # print(num+index)

if __name__ == '__main__': 
    video_path = 'E:\MicrosoftVSCode\projects\Bilibili_downloader-1\video\【三好杯淘汰赛】能源vs公管'
    # files = glob.glob(os.path.join(video_path, '*.ts'))
    # with alive_bar(len(files), title="合成视频", bar="bubbles", spinner="classic") as bar:
    #     for file in files:
    #         cmd = 'ffmpeg -i' + file + 
    #         # with open(file, 'rb') as fr, open(os.path.join(self.video_path, self.title + '.mp4'), 'ab') as fw:
    #         #     content = fr.read()
    #         #     fw.write(content)
    #         # os.remove(file)
    #         bar()


    # aa = range(100)
    # with alive_bar(len(aa), title="合成视频", bar="bubbles", spinner="classic") as bar:
    #     with ThreadPoolExecutor(max_workers=10) as pool:
    #         for index, seg in enumerate(aa):
    #             pool.submit(save_ts, seg, index)
    #             # time.sleep(0.5)
    #             bar()

