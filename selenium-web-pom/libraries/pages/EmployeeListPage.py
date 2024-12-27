from libraries.common.Utils import Utils
from libraries.pages.BasePage import BasePage
from libraries.locators import AddEmployeePageLocators
from libraries.locators import EmployeeListPageLocators
from libraries.common.PageDetailsEnum import PageDetails
from selenium.common.exceptions import NoSuchElementException
from libraries.exceptions.TextFieldNotAvailableException import TextFieldNotAvailableException
from libraries.exceptions.TabElementNotAvailableException import TabElementNotAvailableException
from libraries.exceptions.IconElementNotAvailableExecption import IconElementNotAvailableExecption
from libraries.exceptions.ButtonElementNotAvailableException import ButtonElementNotAvailableException
from libraries.exceptions.CheckBoxElementNotAvailableException import CheckBoxElementNotAvailableException

class   EmployeeListPage(BasePage):
    """ This class holds all the methods that we can do at Apply Leave Page"""
    PAGE_TITLE = PageDetails.EMPLOYEE_LIST_TITLE.value
    PAGE_URL = PageDetails.EMPLOYEE_LIST_URL.value
    PAGE_LOCATOR = EmployeeListPageLocators.XPATH_EMPLOYEE_LIST_TABLE_TXT
    
    def click_employee_list_in_pim(self):
        """Clicks on the 'Employee List' tab in the PIM (Personnel Information Management) section"""
        try:
            super().click_element(EmployeeListPageLocators.XPATH_TAB_EMPLOYEE_LIST_PIM)
        except NoSuchElementException as e:
            raise TabElementNotAvailableException("EmployeeListPage - Employee List") from e

    def enter_employee_name(self,employee_name):
        """Enters the provided employee name into the 'Employee Name' text field"""
        try:
            super().enter_text(EmployeeListPageLocators.XPATH_TXT_EMPLOYEE_NAME,employee_name)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("EmployeeListPage - Employee Name") from e

    def enter_employee_id(self,employee_id):
        """Enters the provided employee id into the 'Employee Id' text field"""
        try:
            super().enter_text(EmployeeListPageLocators.XPATH_TXT_EMPLOYEE_ID,employee_id)
        except NoSuchElementException as e:
            raise TextFieldNotAvailableException("EmployeeListPage - Employee Id") from e

    def click_search(self):
        """Clicks the 'Search' button to initiate a search for employee records"""
        try:
            super().click_element(AddEmployeePageLocators.XPATH_BTN_SEARCH_OR_SAVE)
        except NoSuchElementException as e:
            raise ButtonElementNotAvailableException("EmployeeListPage - Search") from e

    def get_employee_records(self):
        """Retrieves the available employee records from the 'Employee Records' table on the 'Employee List' page"""
        elems = Utils.wait_for_elements(EmployeeListPageLocators.XPATH_TABLE_EMPLOYEE_RECORDS,timeout=3)
        return elems
    
    def no_records_should_be_present(self):
        """Validates that no employee records are present in the 'Employee Records' table"""
        records = self.get_employee_records()

        if records:
            assert False,f"{len(records)} Record(s) is Present"
        else:
            Utils.log_output("No Records is Present")

    def records_should_be_present(self):
        """Validates that at least one employee record is present in the 'Employee Records' table"""
        records = self.get_employee_records()

        if records and len(records)>=1:
            Utils.log_output(f"{len(records)} Record(s) is Present")
        else:
            assert False,"No Records is Present"

    def select_all_records(self):
        """Clicks the 'Select All' checkbox in the 'Employee Records' table"""
        try:
            super().click_element(EmployeeListPageLocators.XPATH_CHECK_BOX_SELECT_ALL)
        except NoSuchElementException as e:
            raise CheckBoxElementNotAvailableException("EmployeeListPage - Select All") from e

    def click_delete_selected(self):
        """Clicks the 'Delete Selected' button to delete the selected employee records"""
        try:
            super().click_element(EmployeeListPageLocators.XPATH_BTN_DELETE)
        except NoSuchElementException as e:
            raise ButtonElementNotAvailableException("EmployeeListPage - Delete Selected") from e

    def click_confirm_delete(self):
        """Clicks the 'Confirm Delete' icon to confirm the deletion of selected employee records"""
        try:
            super().click_element(EmployeeListPageLocators.XPATH_ICON_CONFIRM_DELETE)
        except NoSuchElementException as e:
            raise IconElementNotAvailableExecption("EmployeeListPage - Confirm Delete") from e