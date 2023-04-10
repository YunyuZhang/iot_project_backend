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

       
    def generateURL(self):
        self.app.route("/")(self.test)
        self.app.route('/weight', methods=['GET'])(self.receive_weight)
        self.app.route('/usage', methods=['GET'])(self.receive_usage)
        self.app.route('/getWeight', methods=['GET'])(self.download_weight)
        self.app.route('/getUsage', methods=['GET'])(self.download_usage)

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
        resposne = self.upload_to_firebase(LogType.WEIGHT, dataDict, userID)
        return resposne

    def receive_usage(self):
        dataDict = {
            "usageType": request.args.get('usageType'),
            "timestamp": request.args.get('timestamp'),
            "catName": request.args.get('catName'),
        }
        userID =  request.args.get('userID')
        response = self.upload_to_firebase(LogType.USAGE, dataDict, userID)
        return response
    
    def download_weight(self):
        return self.read_from_firebase(LogType.WEIGHT, request.args.get('userID'))
    
    def download_usage(self):
        return self.read_from_firebase(LogType.USAGE, request.args.get('userID'))
        
    def upload_to_firebase(self, logType, dataDict, userID):
        try:
            ref = db.reference("/" + userID).child(logType.value)
            ref.child(dataDict["timestamp"]).set(dataDict)
            return "log successfully uploaded to DB"
        except Exception as e:
            return "Falied to upload data: ", e
    
    def read_from_firebase(self, logType, userID):
        try:
            ref = db.reference("/" + userID).child(logType.value)
            data = ref.get()
            return data
        except Exception as e:
            return "Falied to download data: ", e


    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    def get_app(self):
        return self.app

# creat app for gunicorn
def create_app():
    my_app = WebServer()
    return my_app.get_app()

if __name__ == "__main__":
    my_app = WebServer()
    my_app.run()


