import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.CourseOverview import CourseOverview


class MentorToolsUtils:
    def __init__(self, driver):
        self.driver = driver

    '''
    Login to MentorTools using the given credentials
    '''
    def login(self, user, password):
        self.driver.get("https://jh-designtester.app.mentortools.com/login")
        # wait for the page to load
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        # type email
        self.driver.find_element(By.ID, "mat-input-0").send_keys(user)
        self.driver.implicitly_wait(10)
        # type password
        self.driver.find_element(By.ID, "mat-input-1").send_keys(password)
        self.driver.implicitly_wait(10)
        # click login
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.text == "Login":
                button.click()
                break
        self.driver.implicitly_wait(10)

    '''
    Get all the courses ids
    '''
    def get_all_courses_ids(self):
        # get all courses
        courseList = self.driver.find_element(By.ID, "CourseList")
        # get all direct children of the course list
        courseListChildrens = courseList.find_elements(By.XPATH, "./*")
        # get all courses ids
        coursesIds = []
        for course in courseListChildrens:
            id = course.get_attribute("id")
            if id is not None and id != "" and id.isdigit():
                coursesIds.append(id)
        return coursesIds

    '''
    Click on the an element with the given id
    '''
    def click_on_element_id(self, id):
        # wait for element to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, id)))
        self.driver.find_element(By.ID, id).click()
        self.driver.implicitly_wait(10)

    '''
    Get all the modules ids
    '''
    def get_modules_ids(self):
        # wait for element ModuleList to load
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.ID, "ModulesList")))
        time.sleep(3)
        # get all modules
        modulesList = self.driver.find_element(By.ID, "ModulesList")
        # get all children of the modules list
        modulesListChildrens = modulesList.find_elements(By.XPATH, "./*")
        # remove the last element (the add module button)
        # get all modules ids
        modulesIds = []
        for module in modulesListChildrens:
            id = module.get_attribute("id")
            # add id only if its a number
            if id is not None and id != "" and id.isdigit():
                modulesIds.append(id)
        return modulesIds

    '''
    Get all the lessons ids
    '''
    def get_lessons_ids(self, moduleId=None):
        # wait for element LessonList to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "LessonsList")))
        time.sleep(3)
        # get all lessons
        if moduleId is not None: # if a module id is given, get the lessons of the module
            module = self.driver.find_element(By.ID, moduleId)
        else: # else get firsts lessons in the page
            module = self.driver
        lessonsList = module.find_element(By.ID, "LessonsList")
        # get all children of the lessons list
        lessonsListChildrens = lessonsList.find_elements(By.XPATH, ".//*")
        # remove the last element (the add lesson button)
        # get all lessons ids
        lessonsIds = []
        for lesson in lessonsListChildrens:
            id = lesson.get_attribute("id")
            if id is not None and id != "" and id.isdigit():
                lessonsIds.append(id)
        return lessonsIds

    '''
    Duplicate the lesson with the given id
    '''
    def duplicateLesson(self, lessonId):
        lessonPanel = self.driver.find_element(By.ID, lessonId)
        # open the dropdown menu
        lessonPanel.find_element(By.ID, "dropdownMenuButton1").click()
        # get all dropdown menu items
        dropdownMenuItems = lessonPanel.find_elements(By.TAG_NAME, "li")
        # click on duplicate
        for item in dropdownMenuItems:
            if item.text == "Duplicate":
                item.click()
                break

    '''
    Create a new course
    :return: the id of the new course
    '''
    def createCourse(self, courseName, courseDescription=None):
        # click on the add course button
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            # text button contains the text "Add new course"
            if "Add new course" in button.text:
                button.click()
                break
        # wait for the course name input to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "title")))
        # type course name
        courseOverview = CourseOverview(self.driver)
        # set course name
        courseOverview.addTitle(courseName)
        # set course description
        if courseDescription is not None:
            courseOverview.addDescription(courseDescription)
        # save and close
        courseOverview.saveAndClose()
        # wait for the course to be created
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CourseList")))
        # return the id of the new course
        return self.get_all_courses_ids()[-1]

    '''
    Create a new module in the course with the given id
    :return: the id of the new module
    '''
    def addModule(self, idCourse, moduleName):
        # click on the course with the given id
        self.click_on_element_id(idCourse)
        time.sleep(1) # wait for the page to load
        # wait for the modules list to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "NewModuleName")))
        # enter the name of the module and press enter
        inputNameModule = self.driver.find_element(By.NAME, "NewModuleName")
        inputNameModule.send_keys(moduleName)
        time.sleep(2)
        inputNameModule.send_keys(Keys.ENTER)
        # wait for the module to be created
        time.sleep(2)
        # return the id of the new module
        return self.get_modules_ids()[-1] # the first module is the new one

    '''
    Create a new lesson in the module with the given id
    :return: the id of the new lesson
    '''
    def addLesson(self, idModule, lessonName):
        # click on the module with the given id
        self.click_on_element_id(idModule)
        # wait for the lessons list to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "NewLessonName")))
        # enter the name of the lesson
        self.driver.find_element(By.NAME, "NewLessonName").send_keys(lessonName)
        # click on the add button
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.text == "Add Lesson":
                button.click()
                break
        # return the id of the new lesson
        return self.get_lessons_ids()[-1] # the last element is the new lesson

    '''
    get name of the course with the given id
    '''
    def get_course_name(self, idCourse):
        course = self.driver.find_element(By.ID, idCourse)
        # find the link with some title inside
        links = course.find_elements(By.TAG_NAME, "a")
        for link in links:
            if link.text is not None and link.text != "":
                return link.text
        raise Exception("No title found for the course with id " + idCourse)

    '''
    Get all courses ids with @test in their name
    '''
    def get_all_test_courses_ids(self):
        # wait for the course list to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CourseList")))
        testCoursesIds = []
        for id in self.get_all_courses_ids():
            if "@test" in self.get_course_name(id):
                testCoursesIds.append(id)
        return testCoursesIds

    '''
    Delete a course with the given id
    '''
    def deleteCourse(self, id):
        # scroll to the course
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.ID, id))
        time.sleep(1) # wait for the scroll to be done
        # wait for the element to load
        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.ID, id)))
        # get the course with the given id
        course = self.driver.find_element(By.ID, id)
        # open the dropdown menu
        # wait for the dropdown menu to load
        WebDriverWait(course, 50).until(EC.presence_of_element_located((By.ID, "dropdownMenuButton1")))
        # scroll to the dropdown menu
        self.driver.execute_script("arguments[0].scrollIntoView();", course.find_element(By.ID, "dropdownMenuButton1"))
        # wait for the dropdown menu to be visible
        WebDriverWait(course, 50).until(EC.element_to_be_clickable(course.find_elements(By.ID, "dropdownMenuButton1")[0]))
        course.find_elements(By.ID, "dropdownMenuButton1")[0].click()
        # get all dropdown menu items
        dropdownMenuItems = course.find_elements(By.TAG_NAME, "li")
        # click on delete
        for item in dropdownMenuItems:
            if item.text == "Move to trash":
                # wait for the element to be clickable
                WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable(item))
                item.click()
                break
        # wait for the information message to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-move-to-trash-message")))
        # select only move to trash message
        moveToTrashMessage = self.driver.find_elements(By.TAG_NAME, "app-move-to-trash-message")[0]
        # click on close (first a)
        moveToTrashMessage.find_elements(By.TAG_NAME, "a")[0].click()
        return True


    '''
    precondition : the source course and the module source must be opened
    Copy the lesson with the given id to 
    '''
    def copyLesson(self, idLesson, courseId, moduleId):
        # wait for the lesson list to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, idLesson)))
        # get the lesson with the given id
        lesson = self.driver.find_element(By.ID, idLesson)
        # open the dropdown menu
        lesson.find_elements(By.ID, "dropdownMenuButton1")[0].click()
        # get all dropdown menu items
        dropdownMenuItems = lesson.find_elements(By.TAG_NAME, "li")
        # click on copy
        for item in dropdownMenuItems:
            if item.text == "Copy to":
                item.click()
                # wait for the copy to modal to load
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "ngb-modal-window")))
                # get into modal windows
                modal = self.driver.find_elements(By.TAG_NAME, "ngb-modal-window")[0]
                # get all courses inputs and click on the one with the given id
                WebDriverWait(modal, 20).until(EC.presence_of_element_located((By.ID, courseId)))
                modal.find_element(By.ID, courseId).click()
                # wait for the module select to load and click on the one with the given id
                WebDriverWait(modal, 20).until(EC.presence_of_element_located((By.ID, moduleId)))
                modal.find_element(By.ID, moduleId).click()
                # click on copy button
                modal.find_element(By.CLASS_NAME, "btn-primary").click()
                return True
        raise Exception("Copy button not found")

    '''
    Click on preview to preview the membership area
    Open the preview with the button in the top right.
    '''
    def previewMembershipArea(self):
        # wait for the menu to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "#help-nav-item")))
        # get a with text "Preview"
        self.driver.find_element(By.LINK_TEXT, "Preview").click()
        # wait for the preview to load
        self.driver.implicitly_wait(10)
        return True

    '''
    Empty the trash of courses
    '''
    def emptyTrash(self):
        # go to deleted courses
        # click on the deleted courses button
        time.sleep(1)
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "Deleted courses" in button.text:
                button.click()
        # while there is no span with written "Trash basket is empty" in the page
        while len(self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Trash basket is empty')]")) == 0:
            # wait for the deleted courses list to load
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CourseList")))
            # click on the delete button witch contain span with class "bi-trash-fill"
            courseList = self.driver.find_element(By.ID, "CourseList")
            # get all children of the course list
            courses = courseList.find_elements(By.XPATH, "./*")
            buttons = courses[0].find_elements(By.TAG_NAME, "a")
            for button in buttons:
                if button.find_elements(By.CLASS_NAME, "bi-trash-fill"):
                    button.click()
                    # wait for delete confirmation modal to load
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
                    confirmMenu = self.driver.find_elements(By.CLASS_NAME, "modal-content")[0]
                    # type delete in the input
                    confirmMenu.find_element(By.TAG_NAME, "input").send_keys("DELETE")
                    #time.sleep(1)
                    # click on delete button
                    buttons = confirmMenu.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        if button.text == "Delete":
                            button.click()
                            time.sleep(1)
                            break
                    break
        # refresh the page
        self.driver.refresh()

