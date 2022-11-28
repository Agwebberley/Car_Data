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

# Create/Update the database.
def create_db():
    # Create the database.

    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cars
                 (id INTEGER PRIMARY KEY, make TEXT, model TEXT, year INTEGER, city TEXT, avgprice INTEGER, results INTEGER, timestamp TEXT)''')
    conn.commit()
    conn.close()
    # Call the function to update the database.
    update_db()

# Update the database.
def update_db():
    # Connect to craigslist and get the data.
    # For each city from cities.txt
    with open('./CarData/cities.txt') as f:
        cities = f.read() 
    cities = cities[1:-2].split(',')
    with open('./CarData/makes.txt') as f:
        makes = f.read()
    makes = makes[1:-2].split(',')
    f.close()
    for city in cities:
        # For each model and year from make_dict.json
        with open('./CarData/make_dict.json') as f:
            make_dict = json.load(f)
        f.close()
        for make in make_dict:
            for model in make_dict[make]:
                # Get the data from craigslist.
                cl = pycraigslist.forsale.cta(site=city[9:-16], filters={'query':f"{make} {model}", 'min_price':1000, 'min_miles': 1000})
                # Get the average price.
                prices = []
                print(f"Getting data for {make} {model} in {city[9:-16]}...")

                for result in cl.search():
                    print(result)
                    try:
                        prices.append(int(result['price']))
                    except:
                        pass
                if len(prices) > 0:
                    avgprice = int(np.mean(prices))
                else:
                    avgprice = 0
                # Get the timestamp.
                # Insert the data into the database.
                conn = sqlite3.connect('cars.db')
                c = conn.cursor()
                now = datetime.now()
                c.execute('''INSERT INTO cars (make, model, city, avgprice, results, timestamp) VALUES (?, ?, ?, ?, ?, ?)''', (make, model, city, avgprice, len(prices), now.strftime('%Y%d%m%H%M%S')))
                conn.commit()
                conn.close()
                time.sleep(0.5)



#update_db()


# Crate cars.db if it doesn't exist.
create_db()


@app.route('/')
def index():
    return flask.render_template('index.html')



#if __name__ == '__main__':
#    app.run(debug=True)

