
'''
Manipulate the customer dashboard
https://jh-designtester.app.mentortools.com/admin/settings/custom-menu
'''
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CustomMenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.navigate_to_design_page()

    '''
    go to design page
    '''
    def navigate_to_design_page(self):
        self.driver.get("https://jh-designtester.app.mentortools.com/admin/settings/custom-menu")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-custom-menu-settings")))
        time.sleep(2)

    '''
    Add an item to the custom menu
    '''
    def add_item(self, name, url):
        # click on Add button
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Add" in button.text:
                button.click()
                # wait for the input fields to load
                time.sleep(2)
                # get the last input with the formcontrolname "name"
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                # fill the name field
                namesinput = []
                for input in inputs:
                    if "name" == input.get_attribute("formcontrolname"):
                        namesinput.append(input)
                namesinput[-1].send_keys(name)
                # fill the url field
                urlsinput = []
                for input in inputs:
                    if "link" == input.get_attribute("formcontrolname"):
                        urlsinput.append(input)
                urlsinput[-1].send_keys(url)
                return
        raise Exception("Add button not found")

    '''
    click on the save button
    '''
    def save(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Save" in button.text:
                button.click()
                time.sleep(1)
                return
        raise Exception("Save button not found")


    '''
    return the number of items in the custom menu
    '''
    def getNumberOfItems(self):
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        # fill the name field
        namesinput = []
        for input in inputs:
            if input is not None and "name" == input.get_attribute("formcontrolname"):
                namesinput.append(input)
        return len(namesinput)


    '''
     Delete an item from the custom menu with the given name
    '''
    def deleteItem(self, name):
        # get input with the name
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for input in inputs:
            if input is not None and name in input.get_attribute('value'):
                # get the parent of parent div
                div = input.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
                # get the delete button
                buttons = div.find_elements(By.CLASS_NAME, "btn")
                for button in buttons:
                    if "Delete" in button.text:
                        button.click()
                        return
                raise Exception("Delete button not found")
        raise Exception("input not found")