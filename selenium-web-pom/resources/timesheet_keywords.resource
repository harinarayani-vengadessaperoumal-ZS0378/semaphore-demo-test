*** Settings ***
Library    ../libraries/pages/TimesheetPage.py
Library    PageObjectLibrary
Library    ../libraries/common/Utils.py
Library    ../libraries/pages/DashboardPage.py
#Library    ../libraries/pages/BasePage.py
Resource    dashboard_page_keywords.resource

*** Variables ***
${TIMESHEET_PAGE_NAME}        TimesheetPage
${TIME_SIDE_MENU_NAME}    Time

*** Keywords ***

Navigate to Timesheet page
    Click "${TIME_SIDE_MENU_NAME}" In Menu
    Wait For Page Load
    The Current Page Should Be  ${TIMESHEET_PAGE_NAME}

Display Employee records from Pending Action Section
    Navigate to Timesheet page
    ${employee_details}=    Get Employee Records From Timesheet Pending Actions
    @{employee_names}=      Set Variable    ${employee_details['Employee Name']}
    ${employee_timeperiods}=    Set Variable    ${employee_details['Timesheet Period']}
    ${count}=               Set Variable    1
    ${employee_count}=    Evaluate    len(${employee_names})

    FOR    ${index}    IN RANGE    0    ${employee_count}
        Log    Employee ${count} name : ${employee_names[${index}]}
        Log    Employee ${count} timeperiod : ${employee_timeperiods[${index}]}
        ${count}=         Evaluate    ${count} + 1
    END