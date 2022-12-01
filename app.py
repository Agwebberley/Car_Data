# Flask web application to display used car data
import flask
import pandas as pd
import numpy as np
import sqlite3
import json
import time
from datetime import datetime
from cartempest import CarTempest
# Create the application.
app = flask.Flask(__name__)

# Create a URL route in our application for "/"
# You can choose a make, model, and year range to search for cars.
@app.route("/")
def index():
    # Get a dictionary of all of the makes, thier corresponding models, and years.
    # Get the data from the database. Filter out cars that all have 0 avgprice and 0 avgmiles.
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars WHERE avgprice > 0 AND avgmiles > 0")
    data = c.fetchall()
    conn.close()
    # Create a dictionary of all of the makes, thier corresponding models, and years.
    makes = []
    for row in data:
        make = row[1]
        if make not in makes:
            makes.append(make)
    makes = sorted(makes)
    return flask.render_template("index.html", makes=makes)

# Create a URL route /_parse_make to parse the data.
@app.route("/_parse_make" , methods=['GET'])
def parse_data():
    # Get the make and return the models.
    make = flask.request.args.get('make', 0, type=str)
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cars WHERE make = ? AND avgprice > 0 AND avgmiles > 0", (make,))
    data = c.fetchall()
    conn.close()
    models = []
    for row in data:
        model = row[2]
        if model not in models:
            models.append(model)
    models = sorted(models)
    return flask.jsonify(result=models)






#if __name__ == '__main__':
#    app.run(debug=True)