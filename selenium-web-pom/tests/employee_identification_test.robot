*** Settings ***
Library         DependencyLibrary
Library         ../libraries/pages/AddEmployeePage.py
Library         ../libraries/pages/DashboardPage.py
Library         ../libraries/common/Setup.py
Variables        ../libraries/common/FilePaths.py

Resource        ../resources/employee_list_page_keywords.resource
Resource        ../resources/login_page_keywords.resource
Resource        ../resources/utility_page_keywords.resource

Suite Setup     Run Keywords  Setting Up The Environment Variable For The Suite
...             AND     Clear Previous Run Results     ${browser}
...             AND  Init Setup And Launch Browser  ${browser}
...             AND  Read JSON
Suite Teardown  Close The Browser

Test Setup      Login with Default User
Test Teardown   Logout the User 

*** Variables ***
${json_file}    ${employee_jsondata_path}
${test_id}      TC_001
${browser}      chrome
${environment}  uat
${FirstName}  
${MiddleName}  
${LastName}  
${EmployeeId}

*** Test Cases ***
Create Employee
    [Documentation]    Test to Create an employee when the empoyee is not exists.

    Create Employee with           ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

Verify Employee Presence
    [Documentation]    Test to Verify the Created employee is present.

    Verify Employee Presence with  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

Delete Employee
    [Documentation]    Test to Delete the Created employee, When the employee is present.

    Depends On Test                Verify Employee Presence
    Delete Employee with           ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

Verify Employee absence
    [Documentation]    Test to Verify the employee is not present, Either the employee is Deleted or not Craeted

    Verify Employee abscence with  ${FirstName}  ${MiddleName}  ${LastName}  ${EmployeeId}

    





    
