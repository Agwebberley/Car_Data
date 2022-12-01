import sqlite3
from cartempest import CarTempest
import json
from datetime import datetime
import numpy as np
import threading
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class DatabaseManager():
    def __init__(self, drivers_number=5):
        self.drivers = []
        self.is_busy = [False for i in range(drivers_number)]
        self.drivers_number = drivers_number
        self.create_db()
        self.create_drivers()
        self.update_db()


    def create_db(self):
        # Create the database.
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS cars
                        (id INTEGER PRIMARY KEY, make TEXT, model TEXT, year INTEGER, results INTEGER, avgprice INTEGER, avgmiles INTEGER, timestamp TEXT)''')
        conn.commit()
        conn.close()
        print('Database created/checked.')
    
    def create_drivers(self):
        # Firefox options.
        op = webdriver.FirefoxOptions()
        op.add_argument('--headless')
        op.add_argument('--no-gpu')
        op.add_argument("start-maximized")
        op.add_argument("disable-infobars")
        op.add_argument("--disable-extensions")
        op.add_argument('--no-sandbox')
        op.add_argument('--disable-application-cache')
        op.add_argument("--disable-dev-shm-usage")
        op.set_preference('permissions.default.image', 2)
        op.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        # Get the path of the Firefox binary. C:\Program Files\Mozilla Firefox\firefox.exe
        op.binary_location = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')

        # Create the drivers.
        for i in range(self.drivers_number):
            driver = webdriver.Firefox(options=op)
            self.drivers.append(driver)
        print('Drivers created.')
    
    def update_db(self):
        # For each model and year from make_dict.json
        with open('make_dict.json') as f:
            make_dict = json.load(f)
        f.close()

        with open('saved.txt') as f:
            saved = f.read()
        f.close()

        saved = saved.split(',')
        # If there is no saved file, start from the beginning.
        if saved == ['']:
            saved = [0, 0, 0]
        # If there is a saved file, start from there.
        else:
            saved = [int(saved[0]), int(saved[1]), int(saved[2])]
        
        # Get the makes from the make_dict. Start from the saved make.
        makes = list(make_dict.keys())[saved[0]:]
        # Start from the saved file.
        for i in range(saved[0], len(makes)):
            make = makes[i]
            for j in range(saved[1], len(make_dict[make])):
                # Get the models from the make_dict.
                model = list(make_dict[make].keys())[j]
                for k in range(saved[2], len(make_dict[make][model])):
                    year = make_dict[make][model][k]
                    # Try to update the database.
                    try:
                        
                        while threading.active_count() >= 5:
                            time.sleep(1)
                        threading.Thread(target=self.threaded_update_db, args=(make, model, year)).start()
                        time.sleep(0.5)
                    # If there is an error (probably TimeOut Error), try again.
                    except:
                        print("Error. Trying again.")                    
                        self.update_db()
                    # Save the current make, model and year.
                    finally:
                        f = open('saved.txt', 'w')
                        f.write(str(i) + ',' + str(j) + ',' + str(k))
                        f.close()
                saved[2] = 0
            saved[1] = 0

    def get_not_busy(self):
        # Get the first driver that is not busy.
        for i in range(self.drivers_number):
            if not self.is_busy[i]:
                return i
        return None                    

    def threaded_update_db(self, make, model, year):

        # Get the driver that is not busy.
        # If there is no driver that is not busy, wait.   
        while self.get_not_busy() == None:
            time.sleep(0.2)
        dn = self.get_not_busy()
        self.is_busy[dn] = True
        driver = self.drivers[dn]
        if driver == None:
            print("Something went wrong.")
        

        # Get the average price & miles.
        print(make, model, year)
        PARAMS = {'make': make.lower().replace(" ", ""), 'model': model.lower().replace(" ", ""), 'minyear': year, 'maxyear': year}
        ct = CarTempest(PARAMS, driver)

        prices = ct.get_prices()
        # Remove $ and commas.
        prices = [int(price[1:].replace(',', '')) for price in prices if price != 'Inquire']
        # Remove Inquire prices.
        prices = [price for price in prices if price != "Inquire"]
        
        results = ct.amount_of_data()
        if len(prices) > 0:
            avgprice = int(np.mean(prices))
        else:
            avgprice = 0
        miles = ct.get_mileages()
        # Remove commas.
        miles = [int(mile[:-4].replace(',', '')) for mile in miles]
        if len(miles) > 0:
            avgmiles = int(np.mean(miles))
        else:
            avgmiles = 0

        # Give the driver back.
        self.is_busy[dn] = False

        # Get the timestamp.
        # Insert the data into the database.
        conn = sqlite3.connect('cars.db')
        c = conn.cursor()
        now = datetime.now()
        c.execute("INSERT INTO cars VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (make, model, year, results, avgprice, avgmiles, now))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    DatabaseManager()