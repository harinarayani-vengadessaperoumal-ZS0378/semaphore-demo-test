from selenium.common.exceptions import NoSuchElementException
from libraries.common.PageDetailsEnum import PageDetails
from libraries.common.Utils import Utils
from libraries.pages.BasePage import BasePage
from libraries.locators import LoginPageLocators
from libraries.locators import TopBarLocators
from libraries.common.Secure import Secure
from libraries.exceptions.TextFieldNotAvailableException import TextFieldNotAvailableException
from libraries.exceptions.ButtonElementNotAvailableException import ButtonElementNotAvailableException

class   LoginPage(BasePage):
    """This class holds all the methods that we can do at Login Page"""
    PAGE_TITLE = PageDetails.LOGIN_TITLE.value
    PAGE_URL = PageDetails.LOGIN_URL.value
    PAGE_LOCATOR = LoginPageLocators.CSS_LOGIN_CONTAINER

    def enter_username(self, username):
        """Type the given text into the username field """
        try:
            super().enter_text(LoginPageLocators.CSS_TXT_USERNAME, username)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("LoginPage - Username") from e

    def enter_password(self, password,private_key=None):
        """Type the given text into the password field"""
        try:
            if private_key:
                super().enter_text(LoginPageLocators.CSS_TXT_PASSWORD,Secure.decrypt_password(password,private_key))
            else:
                super().enter_text(LoginPageLocators.CSS_TXT_PASSWORD, password)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("LoginPage - Password") from e

    def click_the_submit_button(self):
        """Click the submit button, and wait for the page to reload"""
        try:
            super().click_element(LoginPageLocators.CSS_BTN_LOGIN)
            Utils.wait_for_page_load()
        except  NoSuchElementException as e:
            raise ButtonElementNotAvailableException("Login Page - Login") from e

    def is_login_error_displayed(self):
        """is log error displayed"""
        Utils.wait_for_page_load()
        self.selib.capture_page_screenshot()
        return self.is_element_present(LoginPageLocators.CSS_LOGIN_ERROR)
    
    def get_login_error_message(self):
        """get login error"""
        return self.get_value(LoginPageLocators.CSS_LOGIN_ERROR)

    def login(self, username, password):
        """To login to the application"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_the_submit_button()
        Utils.wait_for_page_load()

    def login_message_should_be_displayed(self,message):
        """Verifies that the login result matches the expected outcome."""
        alert = Utils.wait_for_elements(LoginPageLocators.CSS_LOGIN_ERROR,timeout=3)
        if alert:
            self.selib.element_text_should_be(alert[0],str(message))
        else:
            self.selib.element_text_should_be(TopBarLocators.CSS_HEADER_TITLE_TOPBAR,str(message))