
'''
Utility functions for driver
'''
import os
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options


def get_driver():
    # update or download chrome driver
    chromedriver_autoinstaller.install()
    # create a new instance of the Chrome driver
    # set download directory
    chromeOptions = Options()
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-gpu")
    # set the size of the window
    chromeOptions.add_argument("--window-size=1920x1080")
    # chang binay location
    # if os is windows
    if os.name != 'nt':
        chromeOptions.add_argument("--headless")
        chromeOptions.binary_location = "/usr/bin/chromium"
    prefs = {'download.default_directory': os.getcwd()}
    chromeOptions.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(options=chromeOptions)