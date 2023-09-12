from flask import Flask, render_template, request
from datetime import datetime
import pymongo

app = Flask(__name__, static_folder='static')

if __name__ == '__main__':
    app.run(debug=True)