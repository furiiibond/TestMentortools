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
    Add an item to the custom menu
    Add another item there.
    '''
    def test_add_item_to_custom_menu(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        customMenuPage = CustomMenuPage(driver)
        # save the number of items before adding a new one
        nbItemsBefore = customMenuPage.getNumberOfItems()
        # add a new item
        customMenuPage.add_item("@test item", "http://www.google.com")
        # click on save
        customMenuPage.save()
        # test if the item was added
        self.assertEqual(customMenuPage.getNumberOfItems(), nbItemsBefore + 1)
        # delete the item
        self.test_delete_item_from_custom_menu()

    '''
    Delete an item from the custom menu
    Delete the item you just added.
    '''
    def test_delete_item_from_custom_menu(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        customMenuPage = CustomMenuPage(driver)
        # save the number of items before deleting one
        nbItemsBefore = customMenuPage.getNumberOfItems()
        # delete the item
        customMenuPage.deleteItem("@test item")
        # click on save
        customMenuPage.save()
        # test if the item was deleted
        self.assertEqual(customMenuPage.getNumberOfItems(), nbItemsBefore - 1)



