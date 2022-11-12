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


class TestCaseForCC(unittest.TestCase):

    def login_test(self, driver=None):
        if driver is None:
            driver = get_driver()
        # create coachy scraper
        mentorToolsUtils = MentorToolsUtils(driver)
        # login
        mentorToolsUtils.login("jh+designtester@jakobhager.com", "7512D1666974890155k4154ae")
        # wait for the page to load
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "CourseList")))

    def test_create_lesson(self, courseName = "@test course"):
        driver = get_driver()
        self.login_test(driver)
        # login to mentor tools
        mentorToolsUtils = MentorToolsUtils(driver)
        # keep number of courses before creating a new one
        nbCoursesBefore = len(mentorToolsUtils.get_all_courses_ids())
        # create a new course
        idCourse = mentorToolsUtils.createCourse(courseName)
        # check if the course was created
        self.assertEqual(len(mentorToolsUtils.get_all_courses_ids()), nbCoursesBefore + 1)
        # check the name of the course
        self.assertEqual("@test course" in driver.find_element(By.ID, "CourseList").text, True)
        # add a module
        idModule = mentorToolsUtils.addModule(idCourse, "@test module")
        # check if the module was created
        self.assertEqual("@test module" in driver.find_element(By.ID, "CourseList").text, True)
        # add a lesson
        idLesson = mentorToolsUtils.addLesson(idModule, "@test lesson")
        # check if the lesson was created
        self.assertEqual("@test lesson" in driver.find_element(By.ID, "CourseList").text, True)
        # save the id of the lesson for the next tests
        self.testCourseId = idCourse
        self.testModuleId = idModule
        self.testLessonId = idLesson
        return idCourse, idModule, idLesson


    '''
    Test adding stuf to a lesson
    '''
    def test_add_to_lesson(self, idLesson = None):
        if idLesson == None:
            idCourse, idModule, idLesson = self.test_create_lesson()
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        courseOverview = CourseOverview(driver, idLesson)
        # add a video to the lesson
        courseOverview.addVideoByLink("https://player.vimeo.com/video/472946736?h=de101e423a&amp;app_id=122963")
        # add text to the lesson
        courseOverview.addText(
            "In diesem Video bekommst Du eine Übersicht über die neuen digitalen Geschäftsmodelle der"
            " Zukunft. Schau dir das Video an und danach die restlichen Videos in dem Kurs um Details"
            " zur Umsetzung zu erfahren. Am Ende des Kurses bekommst du noch ein spezielles BONUS-Video, in dem Du die nächsten Schritte zu Deiner Umsetzung erfährst.")
        # add button
        courseOverview.addButton("CLICK HERE", "https://mentortools.com")
        # save lesson
        courseOverview.saveAndClose()

    '''
    Test if the lesson is duplicated correctly
    '''
    def test_duplicate_lesson(self, idCourse = None, idModule = None, idLesson = None):
        if idLesson is None:
            idCourse, idModule, idLesson = self.test_create_lesson()
        driver = get_driver()
        self.login_test(driver)
        # login to mentor tools
        mentorToolsUtils = MentorToolsUtils(driver)
        # click on the course
        mentorToolsUtils.click_on_element_id(idCourse)
        # click on the first module
        mentorToolsUtils.click_on_element_id(idModule)
        # we click on the duplicate button
        mentorToolsUtils.duplicateLesson(idLesson)
        # wait the changes to be saved
        time.sleep(3)
        # check if the lesson was duplicated
        lessonsIds = mentorToolsUtils.get_lessons_ids()
        self.assertEqual(len(lessonsIds), 2)  # we have 2 lessons now

    '''
    test Copy the lesson to another course
    '''
    def test_copy_lesson_to_another_course(self, idCourseSrc = None, idModuleSrc = None, idLesson = None, idCourseDest = None, idModuleDest = None):
        if idLesson is None:
            idCourseSrc, idModuleSrc, idLesson = self.test_create_lesson()
        if idCourseDest is None:
            idCourseDest, idModuleDest, idLessonDest = self.test_create_lesson() # idlessonDest is not used
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        mentorToolsUtils = MentorToolsUtils(driver)
        # go to the destination course
        mentorToolsUtils.click_on_element_id(idCourseDest)
        # go to the destination module
        mentorToolsUtils.click_on_element_id(idModuleDest)
        # calculate the number of lessons before copying
        nbLessonsBefore = len(mentorToolsUtils.get_lessons_ids())
        # close the course by clicking on the course
        mentorToolsUtils.click_on_element_id(idCourseDest)
        # go to source course
        # click on the course
        mentorToolsUtils.click_on_element_id(idCourseSrc)
        # click on the first module
        mentorToolsUtils.click_on_element_id(idModuleSrc)
        # copying the lesson
        mentorToolsUtils.copyLesson(idLesson, idCourseDest, idModuleDest)
        # wait the changes to be saved
        time.sleep(3)
        # check if the lesson was copied
        # close the source course by clicking on it
        mentorToolsUtils.click_on_element_id(idCourseSrc)
        # open the destination course
        mentorToolsUtils.click_on_element_id(idCourseDest)
        # open the destination module
        mentorToolsUtils.click_on_element_id(idModuleDest)
        # check if the lesson was copied
        lessonsIds = mentorToolsUtils.get_lessons_ids()
        self.assertEqual(len(lessonsIds), nbLessonsBefore + 1)  # we have 1 more lesson now

    '''
    Click on preview to preview the membership area
    Open the preview with the button in the top right.
    '''
    def test_open_preview(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        mentorToolsUtils = MentorToolsUtils(driver)
        # click on the preview button
        mentorToolsUtils.previewMembershipArea()
        # check if the preview is opened
        self.assertEqual("Customer preview mode" in driver.find_element(By.TAG_NAME, "app-customer-page-header-navbar").text, True)


    '''
     test delete all test courses
    '''
    def test_delete_all_test_courses(self):
        driver = get_driver()
        self.login_test(driver)
        # login to mentor tools
        mentorToolsUtils = MentorToolsUtils(driver)
        # get all courses ids
        coursesIds = mentorToolsUtils.get_all_test_courses_ids()
        # delete all tests courses
        for id in coursesIds:
            mentorToolsUtils.deleteCourse(id)
        # check if all test courses were deleted
        self.assertEqual(len(mentorToolsUtils.get_all_test_courses_ids()), 0)

    '''
    Create a new course
    Go to the course overview and click on the button to add a new course. Set a title and some description and save it.
    '''
    def test_create_course(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        mentorToolsUtils = MentorToolsUtils(driver)
        # save the number of courses before creating a new one
        nbCoursesBefore = len(mentorToolsUtils.get_all_test_courses_ids())
        # click on the add course button
        mentorToolsUtils.createCourse("@test course", "test course description")
        # test if the course was created
        self.assertEqual(len(mentorToolsUtils.get_all_test_courses_ids()), nbCoursesBefore + 1)

    '''
    Add 3 modules and 2 lessons each
    Add the modules and lessons in the overview
    '''
    def test_add_modules_and_lessons(self):
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        mentorToolsUtils = MentorToolsUtils(driver)
        # create a new course
        idCourse = mentorToolsUtils.createCourse("@test course", "test course description")
        # click on the course
        mentorToolsUtils.click_on_element_id(idCourse)
        # add 3 modules
        for i in range(3):
            # add a module
            idModule = mentorToolsUtils.addModule(idCourse, "test module " + str(i))
            # click on the module
            mentorToolsUtils.click_on_element_id(idModule)
            # add 2 lessons
            for j in range(2):
                # add a lesson
                idLesson = mentorToolsUtils.addLesson(idModule, "test lesson " + str(j))
            # check if the lessons were added
            self.assertEqual(len(mentorToolsUtils.get_lessons_ids(idModule)), 2)
        # test if the modules and lessons were added
        self.assertEqual(len(mentorToolsUtils.get_modules_ids()), 3)

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


    # '''
    # Upload a video in the lesson
    # Check if this works. This is a common problem. Upload different videos in different length and different file formats.
    # '''
    # def test_upload_video_in_lesson(self):
    #     driver = get_driver()
    #     # login to mentor tools
    #     self.login_test(driver)
    #     # create a new lesson
    #     courseName = "@test lesson video upload"
    #     courseId, moduleId, lessonId = self.test_create_lesson(courseName)
    #     # open the lesson
    #     courseOverview = CourseOverview(driver, lessonId)
    #     # add a video
    #     courseOverview.addVideoByFile("./videos/big_buck_bunny.mp4")
    #     # add a second video
    #     courseOverview.addVideoByFile("./videos/bouchon_26.8g_19g_2004.avi")
    #     # save the changes
    #     courseOverview.saveAndClose()
    #     # test in preview,if the videos are there
    #     self.test_check_video(courseName)


    '''
    Preview the course and see if the videos are there
    Check out the new videos.
    '''
    def test_check_video(self, courseName=None):
        if courseName is None:
            return
        driver = get_driver()
        # login to mentor tools
        self.login_test(driver)
        mentorTools = MentorToolsUtils(driver)
        mentorTools.previewMembershipArea()
        # go to customer dashboard
        dashboard = Dashboard(driver)
        # open the course
        dashboard.open_course("@test lesson video upload")
        # click on the button Start Course
        courseView = CourseView(driver)
        # click on start course
        lessonView = courseView.start_course()
        # check if the video is there
        self.assertEqual(lessonView.get_nb_video(), 2)



TestCaseForCC().test_create_lesson()
TestCaseForCC().test_add_to_lesson()
TestCaseForCC().test_duplicate_lesson()
TestCaseForCC().test_delete_all_test_courses()


