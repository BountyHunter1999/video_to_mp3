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
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

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
