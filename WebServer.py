import os
from flask import Flask, jsonify, request, make_response
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
        
        try:
            dataDict = {
                "weightValue": request.args.get('value'),
                "timestamp": request.args.get('timestamp'),
                "catName": request.args.get('catName'),
            }
            userID =  request.args.get('userID')
            message = self.upload_to_firebase(LogType.WEIGHT, dataDict, userID)
            response = self.generate_response(200, message)
            return response
        except Exception as e:
            response = self.generate_response(500, e)
            return response

    def receive_usage(self):
        try:
            dataDict = {
                "usageType": request.args.get('usageType'),
                "timestamp": request.args.get('timestamp'),
                "catName": request.args.get('catName'),
            }
            userID =  request.args.get('userID')
            message = self.upload_to_firebase(LogType.USAGE, dataDict, userID)
            response = self.generate_response(200, message)
            return response
        except Exception as e:
            response = self.generate_response(500, e)
            return response
        
    
    def download_weight(self):
        try: 
            response_body = self.read_from_firebase(LogType.WEIGHT, request.args.get('userID'))
            response = self.generate_response(200, response_body)
            return response
        except Exception as e:
            response = self.generate_response(505, "Error occured when downloading weight")
            return response

    
    def download_usage(self):
        try: 
            message = self.read_from_firebase(LogType.USAGE, request.args.get('userID'))
            response = self.generate_response(200, message)
            return response
        except Exception as e:
            response =  self.generate_response(505, "Error occured when downloading usage")
            return response
    
    def upload_to_firebase(self, logType, dataDict, userID):
        try:
            ref = db.reference("/" + userID).child(logType.value)
            ref.child(dataDict["timestamp"]).set(dataDict)
            return "Successfully upload the log to DB"
        except Exception as e:
            return e
    
    def read_from_firebase(self, logType, userID):
        try:
            ref = db.reference("/" + userID).child(logType.value)
            data = ref.get()
            return data
        except Exception as e:
            return "Falied to download data: ", e
    
    def generate_response(self, status_code, message):
        response = make_response({"response_body": message}, status_code)
        return response


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


