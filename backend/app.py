from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from pymongo import MongoClient
import random
import string
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is not set in Render environment variables")

client = MongoClient(MONGO_URI)
db = client["url_shortener"]
urls_collection = db["urls"]

# Function to generate unique short URLs
def generate_short_url():
    while True:
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not urls_collection.find_one({"short_url": short_url}):
            return short_url

# API: Get all URLs
@app.route('/api/urls', methods=['GET'])
def get_urls():
    urls = list(urls_collection.find({}, {"_id": 0, "long_url": 1, "short_url": 1}))
    return jsonify(urls), 200

# API: Create Short URL
@app.route('/api/shorten', methods=['POST'])
def shorten():
    try:
        data = request.json
        long_url = data.get('long_url')

        if not long_url:
            return jsonify({"error": "Missing long_url"}), 400

        # Check if URL is already shortened
        existing = urls_collection.find_one({"long_url": long_url}, {"_id": 0, "short_url": 1})
        if existing:
            return jsonify(existing), 200

        short_url = generate_short_url()
        urls_collection.insert_one({"long_url": long_url, "short_url": short_url})

        return jsonify({"short_url": short_url}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Redirect Short URL
@app.route('/<short_url>')
def redirect_to_url(short_url):
    url_data = urls_collection.find_one({"short_url": short_url})
    if url_data:
        return redirect(url_data["long_url"], code=302)
    return jsonify({"error": "URL Not Found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Ensure Render uses the correct port
    app.run(debug=False, host="0.0.0.0", port=port)
