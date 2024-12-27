from enum import Enum

class   PageDetails(Enum):
    """ Enum Class to maintain the Title and URL of all the Page """
    LOGIN_TITLE = "OrangeHRM"
    LOGIN_URL = "/auth/login"
    DASHBOARD_TITLE = "OrangeHRM"
    DASHBOARD_URL = "/dashboard/index"
    ADD_EMPLOYEE_TITLE = "pim/addEmployee"
    ADD_EMPLOYEE_URL = "pim/addEmployee"
    EMPLOYEE_LIST_TITLE = "OrangeHRM"
    EMPLOYEE_LIST_URL = "viewEmployeeList"

    TIMESHEET_URL = "/time/viewEmployeeTimesheet"
    TIMESHEET_TITLE = "OrangeHRM"