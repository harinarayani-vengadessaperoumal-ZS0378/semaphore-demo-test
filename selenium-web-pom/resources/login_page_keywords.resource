*** Settings ***    
Library    SeleniumLibrary
Library    PageObjectLibrary
Library    ../libraries/pages/BasePage.py
Library    ../libraries/pages/DashboardPage.py
Library    ../libraries/pages/LoginPage.py
Library    ../libraries/common/Setup.py
Library    ../libraries/common/Utils.py


*** Variables ***
${login_page}        LoginPage
${dashboard_page}    DashboardPage
${username}          Admin
${password}          ixppqmKo+ld/HT10n6Mx/xmdV3MuFTB3YvJpherzS7ypGZMW4RV1QrMS3yb3wnaiqxStCEvysbVsFB9G/L5naQ==
${private_key}       8115653951377471912401421605763249631730926562232736154188192907774568382747996472621015632902789054751694047439353965508366856399131695753012850091906839-65537-235035341863595246803147812804044246777016015611299467791464213176619783948856033691118967115933300942440733625884097335634128690005688473599591411376513-5163076618565029592738592945402438898861938941749042508708132625239033639219954359-1571863939069928067270889311043397064283321243393368509136583835567746721
${invalid_password}  a1dmin123


*** Keywords ***
Login Using Provided Credential 
    [Arguments]  ${username}  ${password}  ${private_key}=${None}

    BasePage.Load Page          ${login_page}
    Enter Username              ${username}
    Enter Password              ${password}  ${private_key}
    Click The Submit Button

Verify Login Is Successful

    ${error_displayed}  Run Keyword And Return Status  Is Login Error Displayed
    Run Keyword If  ${error_displayed}  Fail  Login failed due to incorrect credentials

    # If no error, continue with dashboard verification
    The Current Page Should Be  ${dashboard_page}
    ${is_logged_in}  Run Keyword And Return Status  Is Logged In

    IF  ${is_logged_in}==True
        Log  [PASS] User Logged in successfully, user is on the Dashboard page  level=INFO
    ELSE
        Fail  Login failed due to incorrect credentials
    END

Validate Login Using Provided Credential
    [Arguments]  ${username}  ${password}  ${expected_message}  ${private_key}
    
    Login Using Provided Credential    ${username}  ${password}  ${private_key}
    Login Message Should Be Displayed  ${expected_message}
  
Login with Default User

    Login Using Provided Credential  ${username}  ${password}  ${private_key}
    Wait For Page Load
    The Current Page Should Be       ${dashboard_page}
    
Verify Login Is Unsuccessful
    ${is_logged_in}=    Run Keyword And Return Status    Is Login Error Displayed
    IF    ${is_logged_in} == True
        Log    [PASS] Login failed due to incorrect credentials, user is on the Login page    level=INFO
    ELSE
        Fail    User is logged in and Page is Navigated to Dashboard Page
    END