# Author: Paul Adams

# Date: 7/30/23

# Description: This microservice recieves a JSON object within a request containing user choices
# from the partner application. This service returns the most highly rated car from the external
# dataset.

from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"





"""Attributions:

https://flexiple.com/python/python-get-current-directory/
https://stackoverflow.com/questions/17211188/how-to-create-a-timer-on-python
(second answer)
https://docs.python.org/3/library/csv.html
https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application

"""