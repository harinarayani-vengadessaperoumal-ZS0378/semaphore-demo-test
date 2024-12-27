*** Settings ***
Library  Collections
Library  DatabaseLibrary
Library  JSONLibrary
Library  OperatingSystem
Library  String
Library  ../libraries/common/Utils.py

*** Keywords ***
GetTestData
    [Arguments]  ${json_file}  ${test_id}  

    ${json_object} =  Load Json From File  ${json_file}
    ${testData} =  Set Variable  ${json_object}[${Test_id}][testData]
    RETURN  ${testData}
   
GetVerificationData
    [Arguments]  ${json_file}  ${test_id}

    ${json_object} =  Load Json From File  ${json_file}
    ${verificationData} =  Set Variable  ${json_object}[${Test_id}][verificationData]
    RETURN  ${verificationData}

GetJSONValue
    [Arguments]  ${key}  ${json} 

    Dictionary Should Contain Key  ${json}  ${key}
    RETURN  ${json}[${key}]

Read Configuration From File
    [Arguments]  ${config_file_name}

    &{config_dict} =  Create Dictionary
    ${content}=    Get File  ${EXECDIR}\\selenium-web-pom\\data\\config_data\\${config_file_name}.ini
    @{lines}=  Split to lines  ${content}

    FOR    ${element}    IN    @{lines}
        ${key}  ${value} =  Split String  ${element}  =  1
        ${config_dict}  Set To Dictionary  ${config_dict}  ${key}  ${value}
    END

    RETURN  ${config_dict}

Run Keyword Iteratively
    [Arguments]  ${keyword}  @{varargs}  ${test_iteration_count}=${None}

    ${rows} =  Run Keyword if   "${test_iteration_count}" == "${None}"  Get Length  ${varargs}[0]  ELSE  Set Variable  ${test_iteration_count}
    ${coloumns} =  Get Length  ${varargs}

    FOR    ${row}    IN RANGE    ${rows}
        @{args}  Create List
        FOR    ${coloumn}    IN RANGE    ${coloumns}
            Append To List    ${args}    ${varargs}[${coloumn}][${row}]
        END
        Run Keyword And Ignore Error  ${keyword}  @{args}
    END

Read Data Table
    [Arguments]  ${coloumn}  ${table}

    ${output}  Query  SELECT ${coloumn} FROM ${table};
    ${un_wrapped_output}  Un Wrap  ${output}

    RETURN  ${un_wrapped_output}