from flask import Flask, jsonify, request
from datetime import datetime
import requests
from pymodm import connect, MongoModel, fields
from flask_pymongo import PyMongo
import json



app = Flask(__name__)
app.config['MONGO_DBNAME'] = "images"
app.config['MONGO_URI'] = "mongodb://localhost:27017/images"
mongo = PyMongo(app)



class OriginalImages(MongoModel):
    name = fields.CharField()
    b64_string = fields.CharField()
    upload_timestamp = fields.CharField()
    upload_size = fields.ListField()


class InvertedImages(MongoModel):
    name_inv = fields.CharField()
    b64_string_inv = fields.CharField()
    processed_timestamp = fields.CharField()
    processed_size = fields.ListField()


def init_db():
    print("Connecting to database...")
    connect("mongodb+srv://tongfu:Fu19980311tong"
            "@images-yiprk.mongodb.net/images?retryWrites=true&w=majority")
    print("Connected to database.")


def is_upload_in_database(b64str):

    all_b64str = []
    all_original = OriginalImages.objects.raw({})
    for im in all_original:
        all_b64str.append(im.b64_string)
    if b64str in all_b64str:
        return True
    else:
        return False


def is_inverted_in_database(b64str_inv):

    all_b64str_inv = []
    all_inverted = InvertedImages.objects.raw({})
    for im in all_inverted:
        all_b64str_inv.append(im.b64_string_inv)
    if b64str_inv in all_b64str_inv:
        return True
    else:
        return False


def add_original_to_database(name, b64str, time, size):
    new_original = OriginalImages(name=name,
                                  b64_string=b64str,
                                  upload_timestamp=time,
                                  upload_size=size)
    new_original.save()
    return True


def add_inverted_to_database(name_inv, b64str_inv, time_inv, size_inv):
    new_inverted = InvertedImages(name_inv=name_inv,
                                  b64_string_inv=b64str_inv,
                                  processed_timestamp=time_inv,
                                  processed_size=size_inv)
    new_inverted.save()
    return True


@app.route('/addOriginal', methods=['POST'])
def post_original_data():
    in_dict = request.get_json()
    check_result = is_upload_in_database(in_dict["b64_string"])
    if check_result is False:
        name = in_dict["name"]
        b64str = in_dict["b64_string"]
        time = in_dict["upload_timestamp"]
        size = in_dict["upload_size"]
        add_original_to_database(name, b64str, time, size)
        return "successfully add original", 200
    else:
        return "image already exists", 200


@app.route('/addInverted', methods=['POST'])
def post_inverted_data():
    in_dict = request.get_json()
    check_result = is_inverted_in_database(in_dict["b64_string_inv"])
    if check_result is False:
        name_inv = in_dict["inverted_name"]
        b64str_inv = in_dict["b64_string_inv"]
        time_inv = in_dict["processed_timestamp"]
        size_inv = in_dict["processed_size"]
        add_inverted_to_database(name_inv, b64str_inv, time_inv, size_inv)
        return "successfully add processed", 200
    else:
        return "image already exists", 200


@app.route("/getOriginalNames", methods=["GET"])
def get_original_images():
    images_ori = {}
    images_ori["names_ori"] = []
    all_ori = OriginalImages.objects.raw({})
    for im in all_ori:
        images_ori["names_ori"].append(im.name)
    return jsonify(images_ori)


@app.route("/getInvertedNames", methods=["GET"])
def get_inverted_images():
    images_inv = {}
    images_inv["names_inv"] = []
    all_inv = InvertedImages.objects.raw({})
    for im in all_inv:
        images_inv["names_inv"].append(im.name_inv)
    return jsonify(images_inv)


@app.route("/getOriginalB64", methods=["GET"])
def get_original_b64():
    images_ori = {}
    images_ori["b64_ori"] = []
    all_ori = OriginalImages.objects.raw({})
    for im in all_ori:
        images_ori["b64_ori"].append(im.b64_string)
    return jsonify(images_ori)



if __name__ == "__main__":
    init_db()
    app.run()
