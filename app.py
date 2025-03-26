import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API key from environment variables
API_TOKEN = os.getenv("REPLICATE_API_KEY")
URL = "https://api.replicate.com/v1/predictions"

headers = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json",
}
