import pika
import sys
import os
import time

from pymongo import MongoClient

# we need to get the video files from mongodb
# and also upload the mp3 files into mongodb
import gridfs

from convert import to_mp3


def main():
    # for mongo db host in our local machine
    client = MongoClient("host.minikube.internal", 27017)
    # the above instance of mongoclient will give us access to
    # dbs we have in our mongo database
    db_videos = client.videos
    db_mp3 = client.mp3

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)