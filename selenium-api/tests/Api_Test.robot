*** Settings ***

Library    ../libraries/keywords_definition/BookingApi.py
Resource    ../resources/BookingApi.resource
Suite Setup    Set suite variables and Create New Auth Token
*** Variables ***

${booking_id}    6095
${update_propertykey}    totalprice    

*** Test Cases ***

Create New Booking Details and validate statuscode and response
    [Tags]    TC_001  
    Create New Booking details    expectedStatuscode_OK    

Update All Booking Details and validate statuscode and response
    [Tags]    TC_002
    Update All Booking Details    ${booking_id}    expectedStatuscode_OK    

Update 'Totalprice' property's value from Booking API and validate the response
    [Tags]    TC_003
    Get Booking Details and Update It    ${booking_id}    ${update_propertykey}    expectedStatuscode_OK

Get All Booking ID details and validate statuscode and response
    [Tags]    TC_004
    ${get_bookingdetails_response}    Get All Booking ID details as Response
    Run Keyword And Continue On Failure    Validate Get All Booking ID Response    ${get_bookingdetails_response}
    ${schema_result}    Validate Json Schema    ${get_bookingdetails_response.json()}    ${schema_path}    Get_All_Booking_Details_Response_Schema    
    Should Be True    ${schema_result}    Update Booking details response schema validation is unsuccessfull.
    Log    Get All Booking details validation is successfull      

