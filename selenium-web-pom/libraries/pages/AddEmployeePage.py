from libraries.common.Utils import Utils
from libraries.pages.BasePage import BasePage
from libraries.locators import AddEmployeePageLocators
from libraries.common.PageDetailsEnum import PageDetails
from selenium.common.exceptions import NoSuchElementException
from libraries.exceptions.TextFieldNotAvailableException import TextFieldNotAvailableException
from libraries.exceptions.TabElementNotAvailableException import TabElementNotAvailableException
from libraries.exceptions.ItemElementNotAvailableException import ItemElementNotAvailableException
from libraries.exceptions.ButtonElementNotAvailableException import ButtonElementNotAvailableException

class   AddEmployeePage(BasePage):
    """ This class holds all the methods that we can do at Apply Leave Page"""  
    PAGE_TITLE = PageDetails.ADD_EMPLOYEE_TITLE.value
    PAGE_URL = PageDetails.ADD_EMPLOYEE_URL.value
    PAGE_LOCATOR = AddEmployeePageLocators.XPATH_TXT_ADD_EMPLOYEE_TABLE

    def click_add_employee_in_pim(self):
        """Clicks on the 'Add Employee' tab in the PIM (Personnel Information Management) section"""
        try:
            super().click_element(AddEmployeePageLocators.XPATH_TAB_ADD_EMPLOYEE_PIM)
        except NoSuchElementException as e:
            raise TabElementNotAvailableException("AddEmployeePage - Add Employee") from e

    def enter_first_name(self,first_name):
        """Enters the provided first name into the 'First Name' field on the 'Add Employee' page"""
        try:
            super().enter_text(AddEmployeePageLocators.XPATH_VARIABLE_TXT_NAME.replace('{VARIABLE}','First'),first_name)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("AddEmployeePage - First Name") from e

    def enter_middle_name(self,middle_name):
        """Enters the provided middle name into the 'Middle Name' field on the 'Add Employee' page"""
        try:
            super().enter_text(AddEmployeePageLocators.XPATH_VARIABLE_TXT_NAME.replace('{VARIABLE}','Middle'),middle_name)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("AddEmployeePage - Middle Name") from e

    def enter_last_name(self,last_name):
        """Enters the provided last name into the 'Last Name' field on the 'Add Employee' page"""
        try:
            super().enter_text(AddEmployeePageLocators.XPATH_VARIABLE_TXT_NAME.replace('{VARIABLE}','Last'),last_name)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("AddEmployeePage - Last Name") from e    

    def click_save(self):
        """Clicks the 'Save' button to save the changes or new employee data"""
        try:
            super().click_element(AddEmployeePageLocators.XPATH_BTN_SEARCH_OR_SAVE)
        except NoSuchElementException as e:
            raise ButtonElementNotAvailableException("AddEmployeePage - Save") from e

    def capture_result(self):
        """Captures and logs the toast message result after an action on the 'Employee List' or 'Add Employee' page."""
        try:
            title, message = super().capture_toast_message(AddEmployeePageLocators.XPATH_TOAST_MESSAGE)
            Utils.log_output(f"{title}:{message}")
        except NoSuchElementException as e:
            raise ItemElementNotAvailableException("AddEmployeePage - Toast Message") from e

