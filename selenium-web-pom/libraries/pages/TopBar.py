from libraries.common.Utils import Utils
from libraries.locators import TopBarLocators

class   TopBar:
    """This class holds all the methods that we can do at TopBar of a Page"""
    def __init__(self, base_page):
        # base_page is an instance of BasePage, passed during initialization
        self.base_page = base_page

    def is_logged_in(self):
        """To check whether user is logged in"""
        Utils.wait_for_page_load()
        return self.base_page.is_element_visible(TopBarLocators.CSS_ICON_USERDROPDOWN)
    
    def logout_the_user(self):
        """Logs out the current user from the application"""
        # clicks user dropdown
        self.base_page.click_element(TopBarLocators.CSS_ICON_USERDROPDOWN)
        # clicks logout from the dropdown
        self.base_page.click_element(TopBarLocators.XPATH_LINK_LOGOUT)