#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#display = Display(visible=0, size=(800, 600))
#display.start()

# now Chrome will run in a virtual display.
# you will not see the browser.
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://www.google.com')
print (browser.title)
browser.quit()

#display.stop()