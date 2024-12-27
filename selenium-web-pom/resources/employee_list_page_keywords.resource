*** Settings ***
Library    ../libraries/pages/AddEmployeePage.py
Library    ../libraries/pages/EmployeeListPage.py

Resource   ../resources/dashboard_page_keywords.resource
Resource   ../resources/utility_page_keywords.resource

*** Variables ***
${json_file}    ${CURDIR}\\..\\data\\test_data\\employee.json
${test_id}      TC_001

*** Keywords ***
Navigate to Add Employee In PIM

    Click "Pim" In Menu
    Click Add Employee In Pim

Navigate to Employee List In PIM

    Click "Pim" In Menu
    Click Employee List In Pim

Create Employee with
    [Arguments]  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

    Navigate to Add Employee In PIM
    ${Records}  Ensure Employee Existence  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}
    Run Keyword If  ${Records} == ${None}  Add Employee with  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

Verify Employee Presence with
    [Arguments]  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}
    
    Navigate to Employee List In PIM
    Enter Employee Name  ${FirstName} ${MiddleName} ${LastName}
    Enter Employee Id    ${EmployeeId}
    Click Search
    Records Should Be Present

Delete Employee with 
    [Arguments]  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}
    
    Navigate to Employee List In PIM
    Enter Employee Name  ${FirstName} ${MiddleName} ${LastName}
    Enter Employee Id    ${EmployeeId}
    Click Search
    Select All Records
    Click Delete Selected
    Click Confirm Delete
    Capture Result

Verify Employee abscence with
    [Arguments]  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}
    
    Navigate to Employee List In PIM
    Enter Employee Name  ${FirstName} ${MiddleName} ${LastName}
    Enter Employee Id    ${EmployeeId}
    Click Search
    No Records Should Be Present

Ensure Employee Existence
    [Arguments]  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

    Navigate to Employee List In PIM
    Enter Employee Name  ${FirstName} ${MiddleName} ${LastName}
    Enter Employee Id    ${EmployeeId}
    Click Search
    ${Records}  Get Employee Records
    ${Records_len}  Run Keyword If  ${Records}  Get Length  ${Records}
    Log  ${Records_len} Record\(s\) is available
    RETURN  ${Records_len}
    
Add Employee with
    [Arguments]  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}
    
    Click Add Employee In PIM
    Enter First Name   ${FirstName}
    Enter Middle Name  ${MiddleName}
    Enter Last Name    ${LastName}
    Enter Employee Id  ${EmployeeId}
    Click Save
    Capture Result

Read JSON

    ${testData}    GetTestData  ${json_file}  ${test_id}

    ${FirstName}   GetJSONValue  FirstName   ${testData} 
    ${MiddleName}  GetJSONValue  MiddleName  ${testData}
    ${LastName}    GetJSONValue  LastName    ${testData}
    ${EmployeeId}  GetJSONValue  EmployeeId  ${testData}

    Set Suite Variable  ${FirstName}
    Set Suite Variable  ${MiddleName}
    Set Suite Variable  ${LastName}
    Set Suite Variable  ${EmployeeId}


   



