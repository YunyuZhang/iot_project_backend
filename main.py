import os
from flask import Flask, jsonify, request
app = Flask(__name__)


testJson = [
    { 'name': 'Forrest', 'amount': 5000 }
]

@app.route("/test")
def main():
    return jsonify(testJson)

@app.route('/')
def hello():
    return 'Welcome'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
