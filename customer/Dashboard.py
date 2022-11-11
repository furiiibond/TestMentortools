

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
    def open_course(self, courseName=None):
        # wait for courses list to load
        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.ID, "FreeCourses")))
        # click on the button Open Course of the first course
        coursebox = self.driver.find_elements(By.CLASS_NAME, "course-box")
        # get the button
        # get the first course
        courseSelect = coursebox[0]
        if courseName is not None:
            # get the course with the given name
            for course in coursebox:
                if courseName in course.text:
                    courseSelect = course
                    break
        buttons = courseSelect.find_elements(By.CLASS_NAME, "btn")
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

    '''
    Exit the preview mode
    Click on the button in the top right corner to exit the preview mode.
    '''
    def exit_preview_mode(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "✕" in button.text:
                time.sleep(2)
                button.click()
                # check if i am on the admin page
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CourseList")))
                return True
        raise Exception("Exit preview mode button not found")