*** Settings ***
Library         DatabaseLibrary
Library         OperatingSystem
Library         ../libraries/common/Secure.py
Library         ../libraries/common/Setup.py

Resource        ../resources/login_page_keywords.resource
Resource        ../resources/utility_page_keywords.resource

Suite Setup     Run Keywords  Connect To Database with Encryption
...             AND  Setting Up The Environment Variable For The Suite
...             AND  Clear Previous Run Results     ${browser}
...             AND  Init Setup And Launch Browser  ${browser}
Suite Teardown  Run Keywords  Disconnect From Database  Close The Browser

*** Variables ***
${environment}          uat
${browser}              chrome
${config_file_name}  db_config
${table_name}        Test_Data

*** Test Cases ***
Login to Orange HRM 
    [Documentation]    Test to validate login functionality using MySQL Data Base.
    [Tags]    Disabled
    ${username}            Read Data Table  username          ${table_name}
    ${password}            Read Data Table  password          ${table_name}
    ${expected_message}    Read Data Table  expected_message  ${table_name}
    ${private_key}         Read Data Table  private_key       ${table_name}

    Run Keyword Iteratively  Validate Login Using Provided Credential  ${username}  ${password}  ${expected_message}  ${private_key}

*** Keywords ***
Connect To Database with Encryption
    &{config} =  Read Configuration From File  ${config_file_name}
    ${DBpass} =  Secure.Decrypt Password       ${config}[EncryptedPass]  ${config}[PrivateKey]

    Connect To Database  ${config}[DBmodule]  ${config}[DBname]  ${config}[DBuser]  ${DBpass}  ${config}[DBhost]  ${config}[DBport]
    
