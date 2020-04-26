from flask import Flask, jsonify, request
from datetime import datetime
import requests
from pymodm import connect, MongoModel, fields
from flask_pymongo import PyMongo


app = Flask(__name__)
# app.config['MONGO_DBNAME'] = "images"
# app.config['MONGO_URI'] = "mongodb://localhost:27017/images"
# mongo = PyMongo(app)



class UploadedImages(MongoModel):
    name = fields.CharField()
    b64_string = fields.CharField(primary_key=True)
    upload_timestamp = fields.CharField()
    upload_size = fields.ListField()

class InvertedImages(MongoModel):
    inverted_name = fields.CharField()
    b64_string_inv = fields.CharField(primary_key=True)
    processed_timestamp = fields.CharField()
    processed_size = fields.ListField()


def init_db():
    print("Connecting to database...")
    connect("mongodb+srv://tongfu:Fu19980311tong"
            "@images-yiprk.mongodb.net/images?retryWrites=true&w=majority")
    print("Connected to database.")



def add_images_to_original():
    new_original =UploadedImages(name = "test_image_1.jpg",
                       b64_string = "iVBORw0KGgoAAAANSUhEUgAABD0AAALmCAYAAABB3e+uAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJ",
                       upload_timestamp = "20120303",
                       upload_size = [30,30])
    new_inverted =InvertedImages(inverted_name = "test_image_1.jpg",
                                 b64_string_inv = "iVBORw0KGgoAAAANSUhEUgAABD0AAALmCAYAAABB3e+uAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJ",
                                 processed_timestamp = "20120303",
                                 processed_size = [30,30])
    new_original.save()
    new_inverted.save()



def is_upload_in_database(b64str):

    all_b64str = []
    all_original = OriginalImages.objects.raw({})
    for images in all_original:
        all_b64str.append(images.b64_string)
    if b64str in all_b64str:
        return True




@app.route('/addOriginal/<new_upload>', methods=['POST'])
def post_uploaded_data():
    original_images = mongo.db.OriginalImages
    goal_new = {'name': new_goal}
    if bucketList.find({'name': new_goal}).count() > 0:
        return "Goal Already Exists!"
    else:
        bucketList.insert(goal_new)
        return "Added Goal successfully"



def get_all_countries():
    image_b64str = []
    all_images = Images.objects.raw({})
    for image in all_images:
        if image.home_team not in teams:
            teams.append(game.home_team)
        if game.away_team not in teams:
            teams.append(game.away_team)
        teams.sort()
        for team in teams:
            print(team)


def get_England_home_games():
    england_home = WC_Game.objects.raw({"home_team":"England"})
    print(england_home.count())
    for game in england_home:
        print("{}: {} {} - {} {}".format(game.year. game.home_team,
                                         game.home_team_score, game.away_team,
                                         game.away_team_score))


def get_England_away_games():
    england_away = WC_Game.objects.raw({"away_team": "England"})
    print(england_away.count())
    for game in england_away:
        print("{}: {} {} - {} {}".format(game.year.game.home_team,
                                         game.home_team_score, game.away_team,
                                         game.away_team_score))

def get_England_all_games():
    england_all = WC_Game.objects.raw({"$and": [
        {"year":1958},
        {"$or": [{"home_team": "England"}, {"away_team": "England"}]}
    ]})



if __name__ == "__main__":
    init_db()
    add_images_to_original()

