# Author: Paul Adams

# Date: 7/30/23

# Description: This microservice recieves a JSON object within a request containing user choices
# from the partner application. This service returns the most highly rated car from the external
# dataset.

from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/get_car/", methods=['POST'])
def get_car():
    data = request.json
    print(type(data))
    return "Hello, request recieved."





"""Attributions:

https://flexiple.com/python/python-get-current-directory/
https://stackoverflow.com/questions/17211188/how-to-create-a-timer-on-python
(second answer)
https://docs.python.org/3/library/csv.html
https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
(second answer)
https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files
https://stackoverflow.com/questions/10313001/is-it-possible-to-make-post-request-in-flask
(first answer)
https://pythonbasics.org/flask-http-methods/

"""