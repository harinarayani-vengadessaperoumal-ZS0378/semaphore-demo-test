*** Settings ***
Documentation  Test to validate login functionality using JSON Data

Library        ../libraries/common/Setup.py
Resource       ../resources/login_page_keywords.resource
Resource       ../resources/utility_page_keywords.resource
Suite Setup    Run Keywords    Setting Up The Environment Variable For The Suite
...             AND     Clear Previous Run Results     ${browser}
Test Setup     Init Setup And Launch Browser  ${browser}
Test Teardown  Close The Browser

Test Template  Login to Orange HRM

*** Variables ***
${browser}    chrome
${environment}  uat
${json_file}    ${EXECDIR}\\selenium-web-pom\\data\\test_data\\login.json

*** Test Cases ***
TC_001 Login to Orange HRM  ${json_file}  TC_001
    [Tags]    Smoke

TC_002 Login to Orange HRM  ${json_file}  TC_002

TC_003 Login to Orange HRM  ${json_file}  TC_003

*** Keywords ***
Login to Orange HRM 
    [Arguments]  ${test_id}  ${json_file}
    ${testData}          GetTestData          ${test_id}  ${json_file}
    ${verificationData}  GetVerificationData  ${test_id}  ${json_file}

    ${username}          GetJSONValue  username          ${testData} 
    ${password}          GetJSONValue  password          ${testData}
    ${expected_message}  GetJSONValue  expected_message  ${verificationData}
    ${private_key}       GetJSONValue  private_key       ${testData}

    Validate Login Using Provided Credential  ${username}  ${password}  ${expected_message}  ${private_key}
    




    
