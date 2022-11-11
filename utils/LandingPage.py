

'''
Manipulate the customer dashboard
https://jh-designtester.app.mentortools.com/admin/marketing/landings
'''
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LandingPage:
    def __init__(self, driver):
        self.driver = driver
        self.navigate_to_landing_page()

    '''
    go to landing page
    '''
    def navigate_to_landing_page(self):
        self.driver.get("https://jh-designtester.app.mentortools.com/admin/marketing/landings")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-landing-list")))
        time.sleep(2)


    '''
    get number of landing pages
    '''
    def getNumberOfLandingPages(self):
        return len(self.driver.find_elements(By.ID, "cdk-drop-list-1"))

    '''
    Create a new landing page
    '''
    def newLandingPage(self, title, metadata_description, text, type=None):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "+ Add new landing page" in button.text:
                button.click()
                break
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Title")))
        self.driver.find_element(By.ID, "Title").send_keys(title)
        if type:
            self.selectType(type)
        self.addMetadataDescription(metadata_description)
        self.addIntroText(text)
        self.saveAndClose()

    '''
    add a Intro text to the landing page
    '''
    def addIntroText(self, text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fr-view")))
        self.driver.find_element(By.CLASS_NAME, "fr-view").send_keys(text)

    '''
    add metadata_description
    '''
    def addMetadataDescription(self, metadata_description):
        self.driver.find_element(By.ID, "metadata_description").send_keys(metadata_description)


    '''
    save and close
    '''
    def saveAndClose(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Save & close":
                # wait for the save button to be clickable
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
                button.click()
                # wait for the save to complete
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-landing-list")))
                time.sleep(2)
                return
        raise Exception("Save and close button not found")


    '''
    get nb of landing pages
    '''
    def getNumberOfLandingPages(self):
        try:
            return len(self.driver.find_elements(By.TAG_NAME, "tr"))
        except:
            return 0

    '''
    get test landing page
    '''
    def getTestLandingPageRows(self):
        testLandingPage = []
        for row in self.driver.find_elements(By.TAG_NAME, "tr"):
            if "@test" in row.text:
                testLandingPage.append(row)
        return testLandingPage

    '''
    edit the landing page
    :param row: the row of the landing page to edit
    '''
    def editLandingPage(self, row):
        buttons = row.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Edit" in button.text:
                button.click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Title")))
                return
        raise Exception("Edit button not found")

    '''
    delete the landing page
    '''
    def deleteLandingPage(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Delete" in button.text:
                button.click()
                # wait for delete confirmation modal to load
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
                confirmMenu = self.driver.find_elements(By.CLASS_NAME, "modal-content")[0]
                # type delete in the input
                confirmMenu.find_element(By.TAG_NAME, "input").send_keys("DELETE")
                time.sleep(1)
                # click on delete button
                buttons = confirmMenu.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    if button.text == "Delete":
                        button.click()
                        time.sleep(2)
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-landing-list")))
                        return True
                raise Exception("Delete in menu conf : button not found")
        raise Exception("Delete button not found")


    '''
    select the type of landing page
    '''
    def selectType(self, type):
        # select the type of landing page
        options = self.driver.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.text == type:
                option.click()
                time.sleep(1)
                return
        raise Exception("Type not found")



