

'''
Manipulate the customer dashboard
https://jh-designtester.app.mentortools.com/customer/dashboard
'''
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Dashboard:

    def __init__(self, driver):
        self.driver = driver
        self.navigate_to_dashboard()

    '''
    navigate to the dashboard
    '''
    def navigate_to_dashboard(self):
        self.driver.get("https://jh-designtester.app.mentortools.com/customer/dashboard")
        self.driver.implicitly_wait(10)

    '''
    open a course
    Open the first course in the list of free courses
    '''
    def open_course(self):
        # wait for courses list to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "FreeCourses")))
        # click on the button Open Course of the first course
        coursebox = self.driver.find_elements(By.CLASS_NAME, "course-box")
        # get the first course
        course = coursebox[0]
        # get the button
        buttons = course.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Open course":
                # scroll to the end of the page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(button))
                # click on the button
                button.click()
                return
        raise Exception("Open course button not found")