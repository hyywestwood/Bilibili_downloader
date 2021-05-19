from alive_progress.core.progress import alive_bar
from concurrent.futures import ThreadPoolExecutor
import time

def save_ts(num, index):
    pass
    # print(num+index)


aa = range(100)
with alive_bar(len(aa), title="合成视频", bar="bubbles", spinner="classic") as bar:
    with ThreadPoolExecutor(max_workers=10) as pool:
        for index, seg in enumerate(aa):
            pool.submit(save_ts, seg, index)
            # time.sleep(0.5)
            bar()

