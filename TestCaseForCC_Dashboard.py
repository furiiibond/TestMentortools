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
    Create a course, module, lesson
    '''
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


    # '''
    # Preview the course and see if the videos are there
    # Check out the new videos.
    # '''
    # def test_check_video(self, courseName=None):
    #     if courseName is None:
    #         return
    #     driver = get_driver()
    #     # login to mentor tools
    #     self.login_test(driver)
    #     mentorTools = MentorToolsUtils(driver)
    #     mentorTools.previewMembershipArea()
    #     # go to customer dashboard
    #     dashboard = Dashboard(driver)
    #     # open the course
    #     dashboard.open_course("@test lesson video upload")
    #     # click on the button Start Course
    #     courseView = CourseView(driver)
    #     # click on start course
    #     lessonView = courseView.start_course()
    #     # check if the video is there
    #     self.assertEqual(lessonView.get_nb_video(), 2)


