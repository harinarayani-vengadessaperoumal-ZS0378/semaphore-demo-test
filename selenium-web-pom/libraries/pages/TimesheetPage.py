from libraries.pages.BasePage import BasePage
from libraries.common.Utils import Utils
from libraries.locators import TimesheetPageLocators
from robot.api.deco import keyword
from libraries.common.PageDetailsEnum import PageDetails
from libraries.pages.TopBar import TopBar
from libraries.pages.NavBar import NavBar

class   TimesheetPage(BasePage):

    PAGE_URL = PageDetails.TIMESHEET_URL.value
    PAGE_LOCATOR = TimesheetPageLocators.XPATH_TIMESHEET_CONTAINER
    PAGE_TITLE = PageDetails.TIMESHEET_TITLE.value
    SIDE_MENU_NAME  = "Time"

    def __init__(self):
        super().__init__()

        # Pass the current instance of TimesheetPage (which is a BasePage) to TopBar and NavBar
        self.topbar = TopBar(self)
        self.navbar = NavBar(self)
        
    def click_time_menu(self):
        self.navbar.click_menu(self.SIDE_MENU_NAME)

    @keyword('Get Employee Records From Timesheet Pending Actions')
    def get_employee_records_from_timesheet_pending_actions(self):

        super().scroll_to_element(TimesheetPageLocators.XPATH_TIMESHEET_PENDING_ACTION)
        super().wait_element_iterable(TimesheetPageLocators.XPATH_TIMESHEET_PENDING_ACTION)
        employee_records = super().wait_for_and_get_elements(TimesheetPageLocators.XPATH_EMPLOYEE_RECORD_TABLE)
        emp_record_name = []
        emp_record_timeperiod = []

        for index, record in enumerate(employee_records, start=1):
            record_value = super().get_value(record)
            if index % 2 != 0:
                emp_record_name.append(record_value)
            else:
                emp_record_timeperiod.append(record_value)
        
        employee_name_header = super().get_value(TimesheetPageLocators.XPATH_EMPLOYEE_NAME_TABLEHEADER)
        employee_timeperiod_header = super().get_value(TimesheetPageLocators.XPATH_EMPLOYEE_TIMEPERIOD_TABLEHEADER)
        return {employee_name_header: emp_record_name, employee_timeperiod_header: emp_record_timeperiod}
