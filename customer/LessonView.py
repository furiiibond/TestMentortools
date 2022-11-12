
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
This class represents the course view Exemple of URL :  https://jh-designtester.app.mentortools.com/customer/course?course_id=UMQEXERNBU4N&lesson_id=102784
This also stends for quiz view
'''
class LessonView():

    def __init__(self, driver):
        self.driver = driver

    '''
    click on mark as completed
    :return: True if the button text changed to Completed, False otherwise
    '''
    def mark_as_completed(self):
        # wait for the navigation to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "LessonNavigation")))
        # click on mark as complete
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if "Mark as completed" in button.text:
                button.click()
                # wait for the change to be saved
                time.sleep(1)
                if "Completed" in button.text:
                    return True
                return False
        raise Exception("Mark as completed button not found")

    '''
    number of video in the lesson
    '''
    def get_nb_video(self):
        # wait for the video to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "videoWrapper")))
        time.sleep(1)
        # get the number of video
        videos = self.driver.find_elements(By.CLASS_NAME, "videoWrapper")
        return len(videos)

    '''
    QUIZ
    '''

    '''
    answer a question
    :param response: the response to select
    :return: True if the response is correct, False otherwise
    '''
    def answer_question(self, response):
        # wait for the question to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "quizAnswers")))
        time.sleep(1)
        # get label with the given response in it
        labels = self.driver.find_elements(By.TAG_NAME, "label")
        for label in labels:
            if response in label.text:
                # get the input linked to the label
                idInput = label.get_attribute("for")
                # wait for the input to be clickable
                # click on the input get xpath
                xpath = "//*[@id='" + idInput + "']"
                self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH, xpath))
                # wait for the change to be saved
                time.sleep(1)
                # check if the response is correct by clicking on the button Check
                buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
                for button in buttons:
                    if "Check" in button.text:
                        button.click()
                        # wait for the change to be saved
                        time.sleep(1)
                        # check if the response is correct
                        if "right-answer" in label.get_attribute("class"):
                            return True
                        return False
                raise Exception("Check button not found")
        raise Exception("Response not found")
