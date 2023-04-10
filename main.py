import os
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from enum import Enum


class LogType(Enum):
    WEIGHT = "WeightHistory"
    USAGE = "UsageHistory"

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        self.testJson = [
            { 'name': 'Forrest', 'message': "Server is running" }
        ]
        self.generateURL()
        self.initFirebase()
        self.populateData()

       
    def generateURL(self):
        self.app.route("/")(self.test)
        self.app.route('/weight', methods=['GET'])(self.receive_weight)
        self.app.route('/usage', methods=['GET'])(self.receive_usage)

    def initFirebase(self):
        cred = credentials.Certificate("config/iotprojectbackendtest-firebase-adminsdk-rzhc2-80855871ed.json")

        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': "https://iotprojectbackendtest-default-rtdb.firebaseio.com/"
        })
    
    
    def populateData(self):
        ref = db.reference("/")
        with open("testData.json", "r") as f:
            content = json.load(f)
        ref.set(content)
        print(ref.get())

        

    def test(self):
        return jsonify(self.testJson)

    def receive_weight(self):
        
        dataDict = {
            "weightValue": request.args.get('value'),
            "timestamp": request.args.get('timestamp'),
            "catName": request.args.get('catName'),
        }
        userID =  request.args.get('userID')
        self.upload_to_firebase(LogType.WEIGHT, dataDict, userID)
        return dataDict

    def receive_usage(self):
        dataDict = {
            "usageType": request.args.get('usageType'),
            "timestamp": request.args.get('timestamp'),
            "catName": request.args.get('catName'),
        }
        userID =  request.args.get('userID')
        self.upload_to_firebase(LogType.USAGE, dataDict, userID)
        return dataDict

    def upload_to_firebase(self, logType, dataDict, userID):
        ref = db.reference("/" + userID).child(logType.value)
        ref.child(dataDict["timestamp"]).set(dataDict)
        return logType.value + " uploaded to DB"

    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    my_app = WebServer()
    my_app.run()
