from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()
import pyautogui
import pyperclip

# Now Firefox will run in a virtual display.
# You will not see the browser.
browser = webdriver.Firefox()
browser.get('http://www.google.com')
browser.quit()

display.stop()