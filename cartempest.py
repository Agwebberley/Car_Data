from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class CarTempest:
    def __init__(self, params, driver):

        self.ogparams = params
        self.driver = driver
        self.params = self.validate_params()
        self.vparams = self.valid_params()
        self.url = self.gen_url()
        self.html = self.get_html_no_driver()
        self.titles, self.prices, self.mileages = self.strip_html()
        self.years = self.get_years()
        self.data = self.create_data()

    def get_html(self):
        
        op = webdriver.FirefoxOptions()
        op.add_argument('--headless')
        op.add_argument('--no-gpu')
        op.add_argument("start-maximized")
        op.add_argument("disable-infobars")
        op.add_argument("--disable-extensions")
        op.add_argument('--no-sandbox')
        op.add_argument('--disable-application-cache')
        op.add_argument("--disable-dev-shm-usage")
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        # Get the path of the Firefox binary. C:\Program Files\Mozilla Firefox\firefox.exe
        op.binary_location = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        #op.binary_location = '/usr/bin/brave-browser'
        #prefs = {"profile.managed_default_content_settings.images": 2}
        #op.add_experimental_option("prefs", prefs)
        # Use webdriver_manager to get the latest version of chromedriver
        driver = webdriver.Firefox(options=op, firefox_profile=firefox_profile)

        
        driver.get(self.url)
        html = driver.page_source
        driver.close()
        driver.quit()
        return html
    
    def get_html_no_driver(self):
        self.driver.get(self.url)
        html = self.driver.page_source
        return html

    def gen_url(self):
        # BASE_URL pre-defined sale type to fix problems with auctions not returning price correctly,
        # and to fix problems with milage not being returned correctly sale by and min miles are set
        BASE_URL = "https://autotempest.com/results?zip=91321&radius=300&saletype=classified&saleby=dealer&minmiles=100"
        url = BASE_URL
        print(self.params)
        for key, value in self.params.items():
            url += "&{}={}".format(key, value)
        return url
    
    def strip_html(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        titles = soup.find_all("a", class_="listing-link source-link")
        prices = soup.find_all("div", class_="badge__label label--price")
        mileages = soup.find_all("span", class_="info mileage")
        print("titles: ", len(titles), "prices: ", len(prices), "mileages: ", len(mileages))
        for i in range(len(titles)):
            titles[i] = titles[i].get_text()
            prices[i] = prices[i].get_text()
            mileages[i] = mileages[i].get_text()
        return titles, prices, mileages
    
    def create_data(self):
        data = []
        for i in range(len(self.titles)):
            data.append([self.titles[i], self.prices[i], self.mileages[i], self.years[i]])
        return data
    
    def get_data(self):
        return self.data
    
    def get_titles(self):
        return self.titles
    
    def get_prices(self):
        return self.prices
    
    def get_mileages(self):
        return self.mileages
    
    def get_url(self):
        return self.url
    
    
    def get_params(self):
        return self.params
    def get_years(self):
        return [self.titles[i][37:41] for i in range(len(self.titles))]
    
    def validate_data(self):
        if len(self.titles) == len(self.prices) == len(self.mileages):
            return True
        else:
            return False
    
    def validate_params(self):
        params = self.ogparams.copy()
        for param in params:
            if param not in self.valid_params():
                UserWarning("Invalid parameter: {}".format(param))
                self.ogparams.pop(param)
        return self.ogparams
    
    def valid_params(self):
        PARAMS = ['make', 'model', 'minyear', 'maxyear', 'minprice', 'maxprice', 'minmiles', 'maxmiles']
        return PARAMS
    
    def get_valid_params(self):
        return self.vparams
    
    def amount_of_data(self):
        return len(self.titles)
    

def main():
    print("This is a module, not a program")
    print("Usage: from cartempest import CarTempest")
    print("       car = CarTempest(params)")
    print("       Get the data in the form of a list with the following format:")
    print("       [title, price, mileage, year]")
    print("       data = car.get_data()\n")
    print("       Get all of the car Make and Model data")
    print("       titles = car.get_titles()\n")
    print("       Get the prices of all of the cars")
    print("       prices = car.get_prices()\n")
    print("       Get the years of all of the cars")
    print("       years = car.get_years()\n")
    print("       Get the milages of all of the cars")
    print("       mileages = car.get_mileages()\n")
    print("       Get the url used to get the data")
    print("       url = car.get_url()\n")

    print("       Get available params with car.get_params()")
    print("       params = car.get_params()")

def block_aggressively(route): 
        excluded_resource_types = ["stylesheet", "image", "font"]
        if (route.request.resource_type in excluded_resource_types):
            route.abort()
        else: 
            route.continue_() 

if __name__ == "__main__":
    main()