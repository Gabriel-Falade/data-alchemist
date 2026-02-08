import os
from flask import Flask, request, jsonify
from markitdown import MarkItDown
from dotenv import load_dotenv
import google.genai as genai

# load variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Allows react to talk to server

@app.route('/')
def home():
    return