import os
import time

import pyautogui
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CourseOverview:
    '''
    go to the lesson if id is provided
    '''
    def __init__(self, driver, id=None):
        self.driver = driver
        self.id = id
        # if the course as not been created yet (create page)
        if self.id is not None:
            self.navigate_to_course_overview()


    '''
    go to lesson overview page
    '''
    def navigate_to_course_overview(self):
        self.driver.get("https://jh-designtester.app.mentortools.com/admin/course_overview/lesson/" + self.id)
        self.driver.implicitly_wait(10)

    '''
    Add a video to the course using the given url
    '''
    def addVideoByLink(self, videoUrl):
        # wait for element to load Text = "Add some element"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Add some element']")))
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Add Video":
                button.click()
                break
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cdk-drop-list-0"))) # wait for the video container to load
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for input in inputs:
            if input.get_attribute("placeholder") == "Place video url here":
                input.send_keys(videoUrl)
                break
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Save url":
                button.click()
                return
        raise Exception("Save url button not found")

    '''
    Add a video to the course by uploading a file
    '''
    def addVideoByFile(self, videoPath):
        videoPath = os.path.abspath(videoPath)
        # wait for element to load Text = "Add some element"
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Add some element']")))
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Add Video":
                button.click()
                break
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "video-upload")))
        # using pyautogui to upload the file
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "video-upload"))

        WebDriverWait(self.driver, 10).until(element_present).click()  # This opens the windows file selector

        time.sleep(1)
        pyperclip.copy(videoPath)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        # wait for the video to be uploaded text is video name
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[text()='" + os.path.basename(videoPath) + "']")))

    '''
    Add text to the course
    '''
    def addText(self, text):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Add Text":
                button.click()
                self.addDescription(text)
                return
        raise Exception("Add Test button not found")

    '''
    Add button to the course
    '''
    def addButton(self, text, link):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Add Button":
                button.click()
                break
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "btnText")))
        self.driver.find_element(By.ID, "btnText").send_keys(text)
        self.driver.find_element(By.ID, "btnUrl").send_keys(link)

    '''
    type the title of the course
    '''
    def addTitle(self, title):
        self.driver.find_element(By.ID, "title").send_keys(title)
        # wait a bit
        time.sleep(2)

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
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CourseList")))
                return
        raise Exception("Save and close button not found")

    '''
    add a description to the course
    '''
    def addDescription(self, text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fr-view")))
        self.driver.find_element(By.CLASS_NAME, "fr-view").send_keys(text)





