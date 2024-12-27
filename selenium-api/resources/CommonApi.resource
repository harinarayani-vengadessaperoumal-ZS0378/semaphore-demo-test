*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary
Library    ../libraries/keywords_definition/BookingApi.py

*** Keywords ***

Get Json Data From JsonFile    
    [Arguments]    ${testdatakey}    ${testdatapath}
    ${jsonData}    Read Json Data    ${testdatakey}    ${testdatapath}
    Log    ${jsondata}
    RETURN    ${jsondata}

Validate Statuscode Of API Response
    [Arguments]    ${expectedstatuscode}    ${response}    ${msg}="Statuscode validation of ${response.request.method} method API is unsuccessfull."
    ${actual_status} =    Set Variable   ${response.status_code}
    Run Keyword And Continue On Failure    Should Be Equal As Numbers    ${actual_status}    ${expectedStatusCode}    ${msg}
    Log    Expected status code: '${expectedstatuscode}' Actual Status code: '${actual_status}'
    Run Keyword If    '${actual_status}' != '${expectedstatuscode}'    Fail    ${msg}  

Get Response From POST Request
    [Arguments]    ${endpoint}    ${requestBody}    ${authorization}=None
    ${response}    Set Variable    None
    ${response}=    POST    ${endpoint}    json=${requestBody}
    Log      ${response.json()}  
    RETURN    ${response}      

Get Response From PUT Request
    [Arguments]    ${endpoint}    ${requestBody}    ${authorization}=None
    ${response}    Set Variable    None
    ${response}=    PUT    ${endpoint}    json=${requestBody}    headers=${authorization}
    Log      ${response.json()} 
    RETURN    ${response}

Get Response From GET Request
    [Arguments]    ${endpoint}    ${authorization}=None
    ${response}    Set Variable    None
    ${response}=    GET    ${endpoint}
    Log      ${response.json()}
    RETURN    ${response}

Get Response From DELETE Request
    [Arguments]    ${endpoint}    ${authorization}=None
    ${response}    Set Variable    None
    ${response}=    DELETE    ${endpoint}    headers=${authorization}    
    Log      ${response.json()} 
    RETURN    ${response}

Get Test Case ID From Tags
    [Arguments]  @{tags}
    FOR  ${tag}  IN  @{tags}
        FOR  ${tc}  IN  @{tag}
            ${contains_tc} =    Evaluate    "'TC' in '${tc}'"
            IF  ${contains_tc}
                RETURN  ${tc}
            END
        END
    END
    Log  Test Case ID not found.
    RETURN  None