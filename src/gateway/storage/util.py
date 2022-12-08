import pika
import json


def upload(f, fs, channel, access):
    """
    1. Upload the file to the mongodb database using gridfs
    2. Once the upload is successful put a message into rabbitmq queue
        so that a downstream service when they pull that message from the
        queue can process the upload by pulling it from the mongodb
        - this queue allows for the asynchronous communication flow
            between our Gateway service and the service that
            processes our videos
        - this helps to avoid the need for our gateway service wait
            for an internal service to process the video before being
            able to return a response to the client
    """
    # Put the file to mongodb
    try:
        # if put is successful a file id object is returned
        fid = fs.put(f)
    except Exception as err:  # noqa
        print(err)
        return "Internal Server Error", 500

    # if file was uploaded successfully
    # message to put onto our queue
    message = {
        "video_fid": str(fid),
        "mp3_id": None,
        "username": access["username"]
        }

    # Put the message on the queue
    try:
        channel.basic_publish(
            # using the default exchange
            exchange="",
            # key same as queue name for default exchange
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # make sure our messages are persisted in our queue
                # int the event of pod crash or restart of our pod
                # since our pod for rabbitmq queue is a stateful pod within
                # k8s we need to make sure when messages are added to the
                # queue they're actually persisted
                # even if the queue is durable that doesn't mean the messages
                # will be durable so make them durable we use this
                # configuration to tell the rabbitmq that the msg
                # should be persisted until the message has been
                # removed from the queue
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:  # noqa
        # if we can't put our message into the queue
        # 1. we'll delete the file from mongodb
        # as if there is msg in the queue that file is
        # never going to be processed
        fs.delete(fid)
        return "Internal Server Error", 500
