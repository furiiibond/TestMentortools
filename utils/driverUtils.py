
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
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {'download.default_directory': os.getcwd()}
    chrome_options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(options=chrome_options)