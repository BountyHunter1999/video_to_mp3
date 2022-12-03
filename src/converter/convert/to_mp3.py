import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # empty named temp file in temp dir
    # temp file will be automatically be deleted once we're
    # done with it
    tf = tempfile.NamedTemporaryFile()

    # video contents
    # get video files from gridfs
    # convert the str version of our id into Object
    out = fs_videos.get(ObjectId(message["video_fid"]))

    # add video contents to empty file
    # out has a read method that allows us to read the data stored
    # in out, read the bytes from the file
    tf.write(out.read())

    # convert video file into audio file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write the audio to a file
    tf_path = tempfile.gettempdir() + f"/{message['video_fild']}.mp3"
    audio.write_audiofile(tf_path)

    # save the file to mongo
    with open(tf_path, "rb") as f:
        data = f.read()

        # storing mp3 file in gridfs
        fid = fs_mp3s.put(data)

    # delete the temp file manually
    os.remove(tf_path)

    # update our message
    message["mp3_fid"] = str(fid)

    # put the message on a new queue, mp3 queue
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # if we can't successfully put the msg on the queue
        # saying that there's an mp3 available for that msg
        # then we want to delete the actual mp3 from mongodb too
        # becuz if we don't put the msg on the queue then the file
        # in mongodb the mp3 will never get processed anyway
        # so we need to make sure to remove the mp3 from mongodb
        # if we can't add the msg to the queue
        fs_mp3s.delete(fid)
        return "Failed to publish message"
