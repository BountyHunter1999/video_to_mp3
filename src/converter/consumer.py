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
    # client = MongoClient("host.minikube.internal", 27017)
    client = MongoClient("mongodb", 27017)
    # the above instance of mongoclient will give us access to
    # dbs we have in our mongo database
    db_videos = client.videos
    db_mp3 = client.mp3

    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3 = gridfs.GridFS(db_mp3)

    # rabbitmq connection
    connection = pika.BlockingConnection(
        # service name will resolve into host ip for our
        # rabbitmq service
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()
    
    channel.queue_declare(queue="video")

    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3, ch)
        if err:
            # we didn't receive and process the message so the msg
            # won't be removed from the queue
            # delivery tag identifies the delivery on a channel
            # rabbitmq will know which delivery tag (or msg) hasn't been
            # acknowledged so it'll not remove it from queue
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # configuration to consume our messages from our video queue
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        # a callback fn that is called whenever a msg is pulled from
        # a queue
        on_message_callback=callback,
    )
    
    print("Waiting for messages. To exit press CTRL + C")
    # run our consumer, our consumer will listen on the queue or
    # listening on that channel where our video msgs are being put
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        # gracefully shutdown the process on keyboard interrupt
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)