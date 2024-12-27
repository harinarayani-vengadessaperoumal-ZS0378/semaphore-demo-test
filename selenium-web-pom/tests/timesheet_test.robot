*** Settings ***
Resource    ../resources/login_page_keywords.resource
Resource    ../resources/timesheet_keywords.resource

Library    ../libraries/common/Setup.py

Test Setup    Init Setup And Launch Browser    ${BROWSER}    ${ENVIRONMENT}
Test Teardown     Close The Browser

*** Variables ***
${BROWSER}    chrome
${ENVIRONMENT}    uat
${USERNAME}       Admin
${PASSWORD}       admin123

*** Test Cases ***

TC_UP_01 Display Pending Action Records from Timesheet Page
    [Tags]    Regression
    BasePage.Load Page  LoginPage
    Login Using Provided Credential    ${USERNAME}    ${PASSWORD}
    Verify Login Is Successful

    Display Employee records from Pending Action Section