from flask import Flask
from flask_ngrok import run_with_ngrok

app = Flask(__name__)

from routes import *

if __name__ == '__main__':
    app.run(debug=False)