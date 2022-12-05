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
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


ydl_opts = {
    # 'format': 'bestaudio/best',
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
}

import concurrent.futures


def download(url):
    if type(url) is not list:
        url = [url]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def download_with_ydl(url, ydl):
    if type(url) is not list:
        url = [url]
    ydl.download(url)


urls = [
    "https://youtu.be/rUWxSEwctFU",
    "https://youtu.be/UT5F9AXjwhg",
    "https://youtu.be/lTTajzrSkCw",
    "https://youtu.be/cwjMwmDSKV0",
]

import time
import os
import threading

def start_clean():
    for i in os.listdir():
        if i.endswith("mp4"):
            os.remove(i)

if __name__ == "__main__":
    start_clean()
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download, urls)
    duration = time.time() - start_time
    print(f"Downloaded {len(urls)} in {duration} seconds with threading")
    # Downloaded 4 in 59.12602138519287 seconds with threading

    start_clean()

    print()
    print("Direct download")
    start_time = time.time()
    download(urls)
    duration = time.time() - start_time
    print(f"Downloaded {len(urls)} in {duration} seconds without threading")
    # Downloaded 4 in 111.34024572372437 seconds without threading

    start_clean()

    print()
    thread_list = []
    start_time = time.time()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("download with ydl as root context")
        for url in urls:
            worker = threading.Thread(target=download_with_ydl, args=(url, ydl))
            worker.start()
            thread_list.append(worker)
        for worker in thread_list:
            worker.join()
    duration = time.time() - start_time
    print(f"Downloaded {len(urls)} in {duration} seconds ydl as root context")
    # Downloaded 4 in 59.3468132019043 seconds ydl as root context
