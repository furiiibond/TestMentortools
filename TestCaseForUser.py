import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from customer.CourseView import CourseView
from utils.MentorToolsUtils import MentorToolsUtils
from customer.Dashboard import Dashboard
from utils.driverUtils import get_driver



class TestCaseForUser(unittest.TestCase):

    def login_test(self, driver=None):
        if driver is None:
            driver = get_driver()
        # create coachy scraper
        mentorToolsUtils = MentorToolsUtils(driver)
        # login
        mentorToolsUtils.login("jh+designtester@jakobhager.com", "7512D1666974890155k4154ae")
        # wait for the page to load
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "CourseList")))
        # go to customer dashboard
        mentorToolsUtils.previewMembershipArea()

    '''
    Open a course and click on “Start Course”
    '''
    def test_start_course(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        # go to customer dashboard
        dashboard = Dashboard(driver)
        # open the course
        dashboard.open_course()
        # click on the button Start Course
        courseView = CourseView(driver)
        # click on start course
        courseView.start_course()
        # check if the course is started, if app-customer-course tagname is present
        self.assertEqual("app-lesson-desc" in driver.page_source, True)

