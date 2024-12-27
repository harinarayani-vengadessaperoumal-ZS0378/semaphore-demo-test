*** Settings ***
Library         ExcelLibrary
Library         ../libraries/common/Setup.py

Resource        ../resources/login_page_keywords.resource
Resource        ../resources/utility_page_keywords.resource

Suite Setup     Run Keywords  Setting Up The Environment Variable For The Suite
...             AND  Clear Previous Run Results     ${browser}
...             AND  Init Setup And Launch Browser  ${browser}
...             AND  Login with Default User
Suite Teardown  Close The Browser

Test Setup     Open Excel Document  ${excel_file}  doc_id=doc
Test Teardown  Close Current Excel Document

*** Variables ***
${environment}          uat
${browser}              chrome
${excel_file}    ${CURDIR}\\..\\data\\test_data\\test_data.xlsx 
${menu_sheet}    Menus
${widget_sheet}  Widgets
${coloumn_num}   1


*** Test Cases ***
Verify Menus and Widget of OrageHRM
    [Documentation]    Test to compare Menus and Widget of OrageHRM againt Expected data using excel.
    ...  Continues Execution in case of failures.
    [Tags]    Smoke
    @{expected_menus}    Read Excel Column  ${coloumn_num}  sheet_name=${menu_sheet}
    @{actual_menus}      Get Menus
    Run Keyword And Ignore Error  Compare Using Soft Assert  ${expected_menus}  ${actual_menus}

    @{expected_widgets}  Read Excel Column  ${coloumn_num}  sheet_name=${widget_sheet}
    @{actual_widgets}    Get Widgets 
    Run Keyword And Ignore Error  Compare Using Soft Assert  ${expected_widgets}  ${expected_widgets}



