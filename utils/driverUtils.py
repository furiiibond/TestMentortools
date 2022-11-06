
'''
Utility functions for driver
'''
import os
from selenium import webdriver
import chromedriver_autoinstaller


def get_driver():
    # update or download chrome driver
    chromedriver_autoinstaller.install()
    # create a new instance of the Chrome driver
    # set download directory
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.getcwd()}
    options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(options=options)