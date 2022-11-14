import time
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from customer.CourseView import CourseView
from customer.Dashboard import Dashboard
from settings.CustomMenu import CustomMenuPage
from utils.CourseOverview import CourseOverview
from settings.DesignPage import DesignPage
from utils.LandingPage import LandingPage
from utils.MentorToolsUtils import MentorToolsUtils
from utils.OptinProcessPage import OptinProcessPage
from utils.driverUtils import get_driver


class TestCaseForCC_Dashboard(unittest.TestCase):

    def login_test(self, driver=None):
        if driver is None:
            driver = get_driver()
        # create coachy scraper
        mentorToolsUtils = MentorToolsUtils(driver)
        # login
        mentorToolsUtils.login("jh+designtester@jakobhager.com", "7512D1666974890155k4154ae")
        # wait for the page to load
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "CourseList")))

    '''
    Create a new opt-in landing page
    Go to the landing pages and create a new one.
    '''
    def test_create_opt_in_landing_page(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        landingPage = LandingPage(driver)
        # save the number of landing pages before creating a new one
        nbLandingPagesBefore = landingPage.getNumberOfLandingPages()
        # click on button with the text "+ Add new landing page"
        landingPage.newLandingPage("@test landing page", "test landing page description", "test landing page")
        # test if the landing page was created
        self.assertEqual(landingPage.getNumberOfLandingPages(), nbLandingPagesBefore + 1)

    '''
    test delete all test landing pages
    '''
    def test_delete_all_test_landing_pages(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        landingPage = LandingPage(driver)
        # get all landing pages test rows
        landingPagesRows = landingPage.getTestLandingPageRows()
        # delete all tests landing pages
        while len(landingPagesRows) > 0:
            landingPage.editLandingPage(landingPagesRows[0])
            landingPage.deleteLandingPage()
            landingPagesRows = landingPage.getTestLandingPageRows()
        # check if all test landing pages were deleted
        self.assertEqual(len(landingPage.getTestLandingPageRows()), 0)

    '''
    Change something on the landing page
    Adapt the text a bit and save it.
    '''
    def test_change_landing_page(self):
        # create a new landing page
        self.test_create_opt_in_landing_page()
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        landingPage = LandingPage(driver)
        # get the first landing page row
        landingPageRow = landingPage.getTestLandingPageRows()[0]
        # edit the landing page
        landingPage.editLandingPage(landingPageRow)
        # change text
        landingPage.addMetadataDescription("test change")
        # save the changes
        landingPage.saveAndClose()
        self.assertEqual(True, True)

    '''
    Create a new one-more-step landing page
    Create a simple LP with the type “one more step”.
    '''
    def test_create_one_more_step_landing_page(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        landingPage = LandingPage(driver)
        # save the number of landing pages before creating a new one
        nbLandingPagesBefore = landingPage.getNumberOfLandingPages()
        # click on button with the text "+ Add new landing page"
        landingPage.newLandingPage("@test - One more step", "test landing page description", "test landing page", "One more step page")
        # test if the landing page was created
        self.assertEqual(landingPage.getNumberOfLandingPages(), nbLandingPagesBefore + 1)

    '''
    Create a thank you landing page
    Create a simple LP with the type “thank you page”.
    '''
    def test_create_thank_you_landing_page(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        landingPage = LandingPage(driver)
        # save the number of landing pages before creating a new one
        nbLandingPagesBefore = landingPage.getNumberOfLandingPages()
        # click on button with the text "+ Add new landing page"
        landingPage.newLandingPage("@test landing page thank you", "test landing page description", "test landing page", "Thank you page")
        # test if the landing page was created
        self.assertEqual(landingPage.getNumberOfLandingPages(), nbLandingPagesBefore + 1)

    '''
    Go to the optin-process used (default optin process)
    Set a double optin process and select the one-more-step-page and the thank-you-page. 
    '''
    def test_set_double_optin_process(self):
        # create a new landing page with the type "one more step"
        #self.test_create_one_more_step_landing_page()
        # create a new landing page with the type "thank you page"
        #self.test_create_thank_you_landing_page()
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        optinProcess = OptinProcessPage(driver)
        # click on the default optin process
        optinProcess.openDefaultOptinProcess()
        # set the onemorestep
        optinProcess.selectOneMoreStep("@test - One more step")
        # set the thank you page
        optinProcess.selectThankYouPage("@test landing page thank you")
        # save the changes
        optinProcess.saveAndClose()
        self.assertEqual(True, True)

    '''
    Change the design of the membership area
    Choose an individual design. Change some settings. Save it.
    '''
    def test_change_design_of_membership_area(self):
        #TODO
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        designPage = DesignPage(driver)
        # save page title
        pageTitle = designPage.getPagesTitle()
        designPage.setPagesTitle("@test title")
        designPage.selectCustomTemplate("Business Classic")
        designPage.save()
        driver.refresh()
        self.assertEqual(designPage.getPagesTitle(), "@test title")
        # reset the page title
        designPage.setPagesTitle(pageTitle)
        # reset the template
        designPage.selectCustomTemplate("Main")
        designPage.save()



