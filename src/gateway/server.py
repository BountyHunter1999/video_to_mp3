# gridfs allows us to store large files in mongodb
import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo

from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
# videos is the db
# host.minikube.internal gives access to the local host from within a k8s
# cluster
# server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"
server.config["MONGO_URI"] = "mongodb://mongo:27017/videos"

# this wrap our flask application that allows us to interface with
# mongodb
mongo = PyMongo(server)

# gridfs is going to wrap our mongodb which will enable us to use
# mongodb gridfs
fs = gridfs.GridFS(mongo.db)

#  make connection with our rabittmq queue synchronous
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    if access["admin"]:
        # we allow uploading of a single file
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file is required", 400

        # contains name of file  as key and the file as value
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)

            if err:
                return err
        return "Success!", 200
    else:
        return "Not Authorized", 401


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
