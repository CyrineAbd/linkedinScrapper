from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  


client = MongoClient("mongodb://localhost:27017/")
db = client["linkedin_profiles"]
collection = db["profiles"]

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    profiles = list(collection.find({}, {'_id': 0}))  # Exclude _id
    return jsonify(profiles)

if __name__ == '__main__':
    app.run(debug=True)
