import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from customer.LessonView import LessonView

class CourseView():

    def __init__(self, driver):
        self.driver = driver

    '''
    click on start course
    '''
    def start_course(self):
        # wait for course status bar to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ProgressPanel")))
        time.sleep(5)
        # click on start course
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Start course" in button.text:
                button.click()
                # wait for the course to start
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-customer")))
                time.sleep(2)
                return LessonView(self.driver)
        raise Exception("Start course button not found")