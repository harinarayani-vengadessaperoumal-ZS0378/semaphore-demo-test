*** Settings ***
Library        DataDriver  file=${excel_file}  sheet_name=${sheet_name}
Library        ../libraries/common/Setup.py
Variables        ../libraries/common/FilePaths.py

Resource       ../resources/login_page_keywords.resource

Suite Setup     Run Keywords    Setting Up The Environment Variable For The Suite
...             AND     Clear Previous Run Results     ${browser} 
Test Setup     Init Setup And Launch Browser  ${browser}
Test Teardown  Close The Browser

Test Template  Validate Login Using Provided Credential

*** Variables ***
${excel_file}   ${exceldata_path} 
${sheet_name}   Login Credentials
${environment}          uat
${browser}              chrome
${username}
${password}
${expected_message}
${private_key}

*** Test Cases ***
Validate Login Using Provided Credential
    [Documentation]    Test to validate login functionality using Excel Data.

    ${username}  ${password}  ${expected_message}  ${private_key}


*** Keywords ***
Validate Login Using Provided Credential
    [Arguments]  ${username}  ${password}  ${expected_message}  ${private_key}
    
    BasePage.Load Page                 ${login_page}
    Login Using Provided Credential    ${username}  ${password}  ${private_key}
    Login Message Should Be Displayed  ${expected_message}