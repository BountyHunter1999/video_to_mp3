from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    # 'format': 'bestaudio/best',
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

import concurrent.futures

def download(url):
    if type(url) is not list:
        url = [url] 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)



urls = [
    "https://youtu.be/rUWxSEwctFU",
    "https://youtu.be/UT5F9AXjwhg",
    "https://youtu.be/lTTajzrSkCw",
    "https://youtu.be/cwjMwmDSKV0"
]

import time
import os

if __name__ == "__main__":
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(download, urls)
    duration = start_time - time.time()
    print(f"Downloaded {len(urls)} in {duration} seconds with threading")
    
    for i in os.listdir():
        if i.endswith("mp4"):
            os.remove(i)
    print("Direct download")
    start_time = time.time()
    download(urls)
    duration = start_time - time.time()
    print(f"Downloaded {len(urls)} in {duration} seconds without threading")

