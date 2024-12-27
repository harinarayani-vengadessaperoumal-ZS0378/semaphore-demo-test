*** Settings ***

Resource    ../resources/login_page_keywords.resource
Library    ../libraries/common/Setup.py
Library    SeleniumLibrary

Suite Setup     Run Keywords    Setting Up The Environment Variable For The Suite
...             AND     Clear Previous Run Results     ${browser}
Test Setup    Init Setup And Launch Browser    ${browser} 
Test Teardown    Close browser and save logs on Failure

*** Keywords ***
Close browser and save logs on Failure
    Run Keyword If Test Failed    Capture Network Logs On Failure
    Close The Browser
                         
*** Variables ***
${browser}    chrome
${environment}    uat
${username}    Admin
${password}    admin123
${invalid_password}    a1dmin123
${button_locator}    xpath=//button[@title='Apply Leave']
${expected_url_part}    applyLeave
${apply_leave_locator}    xpath=//div[@class='oxd-select-wrapper']
${login_page_name}           LoginPage

${invalid_username_1}    Testing_01
${invalid_password_1}    pwd_01
${invalid_username_2}    Testing_02
${invalid_password_2}    pwd_02
${invalid_username_3}    Testing_03
${invalid_password_3}    pwd_03

*** Test Cases ***
TC01 Login with valid credentials
    [Documentation]    Test to validate login functionality.
    [Tags]    Smoke
    BasePage.Load Page    ${login_page_name}
    ${username}    Retrieve Environment Variable    WEB_APP_USERNAME    
    Login Using Provided Credential    ${username}    ${password}
    Verify Login Is Successful
    Click Button    ${button_locator}
    Wait For Condition    return document.readyState == "complete"
    Location Should Contain    ${expected_url_part}
    ${status}    ${result}=    Run Keyword And Ignore Error    Wait Until Page Contains Element    ${apply_leave_locator}    timeout=10s

    Capture Page Screenshot
    Run Keyword If    "${status}" == "FAIL"    Log    "Failed to find the element within the timeout period."    ERROR

TC02 Login with another credentials
    [Documentation]    Test to validate login functionality with another credential.
    # Added this test to have a Failed Test case
    [Tags]    Regression
    BasePage.Load Page    ${login_page_name}
    Login Using Provided Credential    ${username}    ${invalid_password}
    Verify Login Is Successful

TC03 Verify Login Is Unsuccessfull Using Invalid Credentials - 1
    [Documentation]    Test to validate login functionality using invalid credential.
    [Tags]    Smoke
    BasePage.Load Page    ${login_page_name}
    Login Using Provided Credential    ${invalid_username_1}    ${invalid_password_1}
    Verify Login Is Unsuccessful

TC04 Verify Login Is Unsuccessfull Using Invalid Credentials - 2
    [Documentation]    Test to validate login functionality using invalid credential.
    [Tags]    Invalid_Credentials
    BasePage.Load Page    ${login_page_name}
    Login Using Provided Credential    ${invalid_username_2}    ${invalid_password_2}
    Verify Login Is Unsuccessful

TC05 Verify Login Is Unsuccessfull Using Invalid Credentials - 3
    [Documentation]    Test to validate login functionality using invalid credential.
    [Tags]    Invalid_Credentials
    BasePage.Load Page    ${login_page_name}
    Login Using Provided Credential    ${invalid_username_3}    ${invalid_password_3}
    Verify Login Is Unsuccessful