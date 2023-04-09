import os
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        self.userID = "yunyuzhang11"

        self.testJson = [
            { 'name': 'Forrest', 'amount': 5000 }
        ]

        self.generateURL()
        self.initFirebase()
        self.upload_to_firebase()

       
    def generateURL(self):
        self.app.route("/test")(self.main)
        self.app.route('/')(self.hello)
        self.app.route('/weight', methods=['GET'])(self.receive_weight)
        self.app.route('/usage', methods=['GET'])(self.receive_usage)

    def initFirebase(self):
        cred = credentials.Certificate("config/iotprojectbackendtest-firebase-adminsdk-rzhc2-80855871ed.json")

        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': "https://iotprojectbackendtest-default-rtdb.firebaseio.com/"
            })
        ref = db.reference("/")
        with open("testData.json", "r") as f:
            content = json.load(f)
        ref.set(content)
        print(ref.get())
        

    def main(self):
        return jsonify(self.testJson)

    def hello(self):
        return 'Welcome'

    def receive_weight(self):
        weight = request.args.get('value')
        timestamp = request.args.get('timestamp')
        catName = request.args.get('catName')

        return f'Current weight: {weight}, {timestamp}, {catName}'

    def receive_usage(self):
        timestamp = request.args.get('timestamp')
        cat_name = request.args.get('catName')
        usageType = request.args.get('usageType')
        return f'{timestamp}, {cat_name}, {usageType}'

    def upload_to_firebase(self):
        newData = {
                    "timestamp": "2022-07-16 11:11:11",
                    "eventType": "poop",
                    "catName": "Haybe"
                }
        ref = db.reference("/" + self.userID).child("UsageHistory")
        ref.child("2022-07-16 11:11:11").set(newData)
        return

    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    my_app = WebServer()
    my_app.run()
