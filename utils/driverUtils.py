
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
    chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-setuid-sandbox")

    chromeOptions.add_argument("--remote-debugging-port=9222")  # this

    chromeOptions.add_argument("--disable-dev-shm-using")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_argument("--headless")
    prefs = {'download.default_directory': os.getcwd()}
    chromeOptions.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(options=chromeOptions)