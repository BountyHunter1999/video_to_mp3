import pika
import sys
import os
import time

from send import email

def main():
    # rabbitmq connection
    connection = pika.BlockingConnection(
        # service name will resolve into host ip for our
        # rabbitmq service
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()
    
    channel.queue_declare(queue=os.environ.get("VIDEO_QUEUE"), durable=True)
    channel.queue_declare(queue=os.environ.get("MP3_QUEUE"), durable=True)

    def callback(ch, method, properties, body):
        err = email.notification(body)
        if err:
            # we didn't receive and process the message so the msg
            # won't be removed from the queue
            # delivery tag identifies the delivery on a channel
            # rabbitmq will know which delivery tag (or msg) hasn't been
            # acknowledged so it'll not remove it from queue
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # configuration to consume our messages from our mp3 queue
    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
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