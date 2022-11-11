
'''
Manipulate the customer dashboard
https://jh-designtester.app.mentortools.com/admin/settings/design
'''
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DesignPage:
    def __init__(self, driver):
        self.driver = driver
        self.navigate_to_design_page()

    '''
    go to design page
    '''
    def navigate_to_design_page(self):
        self.driver.get("https://jh-designtester.app.mentortools.com/admin/settings/design")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-configure-design")))

    '''
    set Pages Title
    '''
    def setPagesTitle(self, title):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Subtitle")))
        self.driver.find_element(By.ID, "Subtitle").clear()
        self.driver.find_element(By.ID, "Subtitle").send_keys(title)


    '''
    click on the custom tamplate with the given name
    '''
    def selectCustomTemplate(self, name):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hide-radio")))
        radioButtons = self.driver.find_elements(By.CLASS_NAME, "hide-radio")
        for radioButton in radioButtons:
            if name in radioButton.text:
                radioButton.find_element(By.TAG_NAME, "input").click()
                return
        raise Exception("Custom template not found")


    '''
    click on the save button
    '''
    def save(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Save" in button.text:
                button.click()
                return
        raise Exception("Save button not found")

    '''
    return the name of pages title
    '''
    def getPagesTitle(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Subtitle")))
        return self.driver.find_element(By.ID, "Subtitle").get_attribute("value")
