*** Settings ***
Library    ../libraries/common/PropertiesFileReader.py
Library    ../libraries/common/Decryption.py
Library    ../libraries/common/CommonUtilities.py
Library    ../libraries/keywords_definition/BookingApi.py
Library    SeleniumLibrary
Library    RequestsLibrary
Resource    ../resources/CommonApi.resource

*** Variables ***

#Path variables
${schema_path}    ${EXECDIR}//selenium-api//data//schemas//api_schema.json
${api_testdata_filepath}    ${EXECDIR}//selenium-api//data//api_testdata.json
${api_request_filepath}    ${EXECDIR}//selenium-api//data//api_request.json

#URL variables
${update_booking_url}
${create_token_url}
${new_booking_url}
${get_booking_details_url}
${delete_booking_url}

${create_token_response}
${create_token_requestBody}
${headers}

*** Keywords ***

Initialize variables
    ${create_token_url}    Get Value From Properties File    createToken_Url
    Set Suite Variable    ${create_token_url}    ${create_token_url}
    ${new_booking_url}    Get Value From Properties File    newBooking_Url
    Set Suite Variable    ${new_booking_url}    ${new_booking_url}
    ${get_booking_details_url}    Get Value From Properties File    getBookingDetails_URL
    Set Suite Variable    ${get_booking_details_url}    ${get_booking_details_url}
    ${create_token_requestBody}    Get Json Data from JsonFile    CreateToken_Request    ${api_request_filepath}    
    Set Suite Variable    ${create_token_requestBody}    ${create_token_requestBody}
    ${update_booking_url}    Get Value From Properties File    updateBooking_URL  
    Set Suite Variable    ${update_booking_url}    ${update_booking_url}
    ${delete_booking_url}    Get Value From Properties File    deleteBooking_URL   
    Set Suite Variable    ${delete_booking_url}    ${delete_booking_url}

Set suite variables and Create New Auth Token
    Initialize variables
    Create and validate Token
    Set Header for API

Decrypt Password and Update Create Token Requestbody
    ${encrypted_password}    Get Value From Properties File    encrypted_Password
    ${privatekey}    Get Value From Properties File    privateKey
    ${decrypted_password}    Decrypt The Value    ${encrypted_password}    ${privatekey}    
    ${json_request}=    Update Json Data    password    ${decrypted_password}    ${create_token_requestBody}   
    RETURN    ${json_request}
    
Create And Validate Token 
    ${create_token_expected_statuscode}    Get Json Data from JsonFile    expectedStatuscode_OK    ${api_testdata_filepath}
    ${requestbody}    Decrypt Password and Update Create Token Requestbody
    ${create_token_response}=    Get Response From POST Request    ${createToken_URL}    ${requestBody}
    Run Keyword And Continue On Failure   Validate Statuscode of API response    ${create_token_expected_statuscode}    ${create_token_response}
    Set Suite Variable    ${create_token_response}    ${create_token_response}
    ${result}=    Validate CreateToken Response    ${create_token_response}
    Should Be True    ${result}    Create Token Response validation is unsuccessfull
    ${schema_result}    Validate Json Schema    ${create_token_response.json()}    ${schema_path}    Create_Auth_Token_Response_Schema    
    Should Be True    ${schema_result}    Create Token Response schema validation is unsuccessfull 
    Log    Token creation and validation is successfull    

Set Header for API
    ${tokenValue}    Get Property Value From Response    ${create_token_response}    token
    ${headers}    Create Dictionary    cookie=${tokenValue}
    Set Suite Variable    ${headers}    ${headers}
    Log    ${headers}

Create New Booking details
    [Arguments]    ${testdatakey}
    ${testcase_id}=    Get Test Case ID from Tags    ${TEST_TAGS}
    ${testdata}    Get TestData    ${api_testdata_filepath}    ${testcase_id}    ${testdatakey}        
    ${create_newbooking_expectedstatuscode}    Set Variable If    "${testdata}"!="None"    ${testdata}   
    ${create_newbooking_request}    Generate CreateBookingDetails Request 
    ${create_newbooking_response}=    Get response from POST request    ${newBooking_Url}    ${create_newbooking_request}    ${headers}
    Run Keyword And Continue On Failure    Validate Statuscode of API response    ${create_newbooking_expectedstatuscode}    ${create_newbooking_response}
    ${result}=    Validate Createbookingdetails Response    ${create_newbooking_request}    ${create_newbooking_response}
    Run Keyword If    '${result}'!='True'    Fail    Create new Booking details response validation is unsuccessfull.
    ${schema_result}    Validate Json Schema    ${create_newbooking_response.json()}    ${schema_path}    Create_Booking_Response_Schema    
    Run Keyword If    '${schema_result}'!='True'    Fail    Create new Booking details schema validation is unsuccessfull.
    Log    New booking creation and validation is successfull

Update All Booking Details
    [Arguments]    ${bookingId}    ${testdatakey}
    ${testcase_id}=    Get Test Case ID From Tags    ${TEST_TAGS}
    ${testData}    Get TestData    ${api_testdata_filepath}    ${testcase_id}    ${testdatakey}        
    ${update_booking_expected_statuscode}    Set Variable If    "${testData}"!="None"    ${testData}  
    ${request}    Generate Updateallbookingdetails Request
    ${update_response}    Get response from PUT request    endpoint=${update_booking_url}${bookingId}    requestBody=${request}    authorization=${headers}
    Run Keyword And Continue On Failure    Validate Statuscode of API response    ${update_booking_expected_statuscode}    ${update_response}
    ${result}=    Validate Update Booking Details Response    ${request}    ${update_response}
    Run Keyword If    '${result}'!='True'    Fail    Update all Booking details response validation is unsuccessfull.
    ${schema_result}    Validate Json Schema    ${update_response.json()}    ${schema_path}    Update_Booking_Response_Schema    
    Run Keyword If    '${schema_result}'!='True'    Fail    Update all Booking details response schema validation is unsuccessfull.    
    Log    Updating All Booking Details and Validation is successfull

Get Booking Details and Update It
    [Arguments]    ${bookingId}    ${propertykey}    ${testdatakey}
    ${get_details_endpoint}    Set Variable    ${get_booking_details_url}${bookingId}
    ${testcase_id}=    Get Test Case ID from Tags    ${TEST_TAGS}
    ${testdata}    Get TestData    ${api_testdata_filepath}    ${testcase_id}    ${testdatakey}        
    ${get_booking_details_expected_statuscode}    Set Variable If    "${testdata}"!="None"    ${testdata}  
    ${get_bookingdetails_response}    Get Response From GET Request    ${get_details_endpoint}    ${get_booking_details_expected_statuscode}            
    ${request}    Update Booking Details Of Specific Property    ${propertykey}    ${get_bookingdetails_response.json()}    
    ${update_booking_expected_statuscode}    Set Variable If    "${testdata}"!="None"    ${testdata}  
    ${update_response}    Get Response From PUT Request    ${update_booking_url}${bookingId}    ${request}    ${headers}
    Run Keyword And Continue On Failure    Validate Statuscode of API response    ${update_booking_expected_statuscode}    ${update_response}
    ${result}=    Validate Update Booking Details Response    ${request}    ${update_response}
    Run Keyword If    '${result}'!='True'    Fail    Update Booking details response validation is unsuccessfull.
    ${schema_result}    Validate Json Schema    ${update_response.json()}    ${schema_path}    Update_Booking_Response_Schema    
    Run Keyword If    '${schema_result}'!='True'    Fail    Update Booking details response schema validation is unsuccessfull.
    Log    Updating '${propertykey}' property from booking details and Validation is successfull

Get All Booking ID details as Response
    ${get_bookingdetails_expected_statuscode}    Get Json Data from JsonFile    expectedStatuscode_OK    ${api_testdata_filepath}    
    ${get_bookingdetails_response}    Get Response From GET Request    ${get_booking_details_url}    ${get_bookingdetails_expected_statuscode}            
    RETURN    ${get_bookingdetails_response}

Delete Existing Booking Details
    [Arguments]    ${bookingId}    ${testdatakey}
    ${get_details_endpoint}    Set Variable    ${get_booking_details_url}${bookingId}
    ${testcase_id}=    Get Test Case ID from Tags    ${TEST_TAGS}
    ${testdata}    Get TestData    ${api_testdata_filepath}    ${testcase_id}    ${testdatakey}        
    ${get_bookingdetails_expected_statuscode}    Set Variable If    "${testData}"!="None"    ${testData}  
    ${get_bookingdetails_response}    Get response from GET request    ${get_details_endpoint}    ${get_bookingdetails_expected_statuscode}            
    ${schema_result}    Validate Json Schema    ${get_bookingdetails_response.json()}    ${schema_path}    Update_Booking_Response_Schema    
    Run Keyword If    '${schema_result}'!='True'    Fail    Get Booking details response schema validation is unsuccessfull.
    ${delete_booking_expected_statuscode}    Get Json Data from JsonFile    expectedStatuscode_OK    ${api_testdata_filepath}    
    ${delete_endpoint}    Set Variable    ${deleteBooking_URL}${bookingId}
    ${delete_bookingdetails_response}    Get response from DELETE request    ${delete_endpoint}    ${headers}            
    ${result}    Validate Delete BookingDetails Response    ${delete_bookingdetails_response}
    Run Keyword If    '${result}'!='True'    Fail    Delete booking details validation is unsuccessfull    
    Log    Delete booking details and response validation is successfull

Delete booking details
    ${get_bookingdetails_response}    Get All Booking ID details as Response
    ${result}    Validate Get All Booking ID Response    ${get_bookingdetails_response}
    Delete All booking details    ${get_bookingdetails_response}