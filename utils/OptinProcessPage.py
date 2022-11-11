

'''
Manipulate the customer dashboard
https://jh-designtester.app.mentortools.com/admin/marketing/opt-ins
'''
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OptinProcessPage:
    def __init__(self, driver):
        self.driver = driver
        self.navigate_to_optin_process_page()

    '''
    go to optin process page
    '''
    def navigate_to_optin_process_page(self):
        self.driver.get("https://jh-designtester.app.mentortools.com/admin/marketing/opt-ins")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-optins")))

    '''
    open default optin process
    '''
    def openDefaultOptinProcess(self):
        # get span with text "Default system opt-in"
        tds = self.driver.find_elements(By.TAG_NAME, "td")
        for td in tds:
            if "Default system opt-in" in td.text:
                td.find_element(By.TAG_NAME, "span").click()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "app-optins-dialog")))
                return
        raise Exception("Default system opt-in not found")

    '''
    in app-optins-dialog select one more step
    '''
    def selectOneMoreStep(self, title):
        time.sleep(1)
        # get select with atribut formcontrolname one_more_step_page_id
        selects = self.driver.find_elements(By.TAG_NAME, "select")
        for select in selects:
            if "one_more_step_page_id" in select.get_attribute("formcontrolname"):
                # get option with text "@test - One more step"
                options = select.find_elements(By.TAG_NAME, "option")
                for option in options:
                    if title in option.text:
                        option.click()
                        return
                raise Exception("One more step not found")
        raise Exception("Select not found")

    '''
    in app-optins-dialog select thank you page
    '''
    def selectThankYouPage(self, title):
        time.sleep(1)
        # get select with atribut formcontrolname thank_you_page_id
        selects = self.driver.find_elements(By.TAG_NAME, "select")
        for select in selects:
            if "thank_you_page_id" in select.get_attribute("formcontrolname"):
                # get option with text "@test - Thank you"
                options = select.find_elements(By.TAG_NAME, "option")
                for option in options:
                    if title in option.text:
                        option.click()
                        return
                raise Exception("Thank you page not found")
        raise Exception("Select not found")

    '''
    save and close
    '''
    def saveAndClose(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, "btn")
        for button in buttons:
            if button.text == "Save & close":
                # wait for the save button to be clickable
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(button))
                button.click()
                # wait for the save to complete
                time.sleep(2)
                # check if url ends with /admin/marketing/opt-ins
                if not self.driver.current_url.endswith("/admin/marketing/opt-ins"):
                    raise Exception("Save failed")
                return
        raise Exception("Save and close button not found")

