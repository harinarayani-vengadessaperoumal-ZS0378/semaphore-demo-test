from libraries.pages.NavBar import NavBar
from libraries.pages.TopBar import TopBar
from libraries.pages.BasePage import BasePage
from libraries.locators import DashboardPageLocators
from libraries.common.PageDetailsEnum import PageDetails
from selenium.common.exceptions import NoSuchElementException
from libraries.exceptions.ItemElementNotAvailableException import ItemElementNotAvailableException
from libraries.exceptions.ButtonElementNotAvailableException import ButtonElementNotAvailableException


class   DashboardPage(BasePage):
    """ This class holds all the methods that we can do at Dashboard Page"""
    PAGE_TITLE = PageDetails.DASHBOARD_TITLE.value
    PAGE_URL = PageDetails.DASHBOARD_URL.value
    PAGE_LOCATOR = DashboardPageLocators.CSS_DASHBOARD_WIDGETS

    def __init__(self):
        super().__init__()

        # Pass the current instance of DashboardPage (which is a BasePage) to TopBar and NavBar
        self.topbar = TopBar(self)
        self.navbar = NavBar(self)

    def is_logged_in(self):
        """To check whether User is Logged In"""
        return self.topbar.is_logged_in()

    def is_dashboard_widget_displayed(self):
        """To check whether Dashboard Widget is displayed"""
        return self.is_element_visible(DashboardPageLocators.CSS_DASHBOARD_WIDGETS)
    
    def get_widgets(self):
        """Retrieve all the widget items in the dashboard"""
        try:
            widgets_elem = self.wait_for_and_get_elements(DashboardPageLocators.XPATH_WIDGETS_HEADERS)
            widgets = [elem.text for elem in widgets_elem]
            return widgets
        except NoSuchElementException as e:
            raise ItemElementNotAvailableException("DashboardPage - Widget") from e
    
    def get_menus(self):
        """Retrieve all the menu items in the navigation bar"""
        try:
            return self.navbar.get_menus()  
        except NoSuchElementException as e:
            raise ItemElementNotAvailableException("DashboardPage - Menu") from e
    
    def click_option_in_quick_launch(self,option):
        """Clicks the provided option in the 'Quick Launch' section on the Dashboard page"""
        try:
            self.click_element(DashboardPageLocators.XPATH_VARIABLE_BTN_QUICK_LAUNCH.replace("{VARIABLE}",option))
        except NoSuchElementException as e:
            raise ButtonElementNotAvailableException(f"DashboardPage - Quick Launch-{option}") from e

    def click_option_in_menu(self,option):
        """Clicks the provided option in the menu of navigation bar"""
        try:
            self.navbar.click_option_in_menu(option)
        except NoSuchElementException as e:
            raise ItemElementNotAvailableException(f"DashboardPage - Menu-{option}") from e

    def logout_the_user(self):
        """Logs out the current user from the application"""
        try:
            self.topbar.logout_the_user()
        except NoSuchElementException as e:
            raise ItemElementNotAvailableException("DashboardPage - logout") from e