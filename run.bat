@echo off
REM Set the number of parallel processes
set PROCESSES=3

REM Specify the tags you want to include and exclude
set INCLUDE_TAGS=SmokeORTC_003
set EXCLUDE_TAGS=Disabled

REM Accept browser name as a parameter or default to chrome
set BROWSER=%1
if "%BROWSER%"=="" set BROWSER=chrome

REM Default to 'head' mode if no argument is passed
SET MODE=%2
IF "%MODE%"=="" SET MODE=head

REM Set single Allure results directory for all tests
set ALLURE_RESULTS=.\output\allure-results
set ALLURE_REPORT=.\output\allure-report

REM Create Allure results directory if it doesn't exist
if not exist "%ALLURE_RESULTS%" mkdir "%ALLURE_RESULTS%"
if not exist "%ALLURE_REPORT%" mkdir "%ALLURE_REPORT%"

REM Run web tests with Allure reporting
echo Running Web Tests...
pabot --processes %PROCESSES% ^
      --testlevelsplit ^
      --variable browser:%BROWSER% ^
      --variable mode:%MODE% ^
      --pythonpath .\selenium-web-pom ^
      --outputdir .\selenium-web-pom\test-results ^
      --include %INCLUDE_TAGS% ^
      --exclude %EXCLUDE_TAGS% ^
      --listener allure_robotframework:"%ALLURE_RESULTS%" ^
      .\selenium-web-pom\tests

REM Run API tests with Allure reporting
echo Running API Tests...
pabot --processes %PROCESSES% ^
      --testlevelsplit ^
      --pythonpath .\selenium-api ^
      --outputdir .\selenium-api\test-results ^
      --include %INCLUDE_TAGS% ^
      --listener allure_robotframework:"%ALLURE_RESULTS%" ^
      .\selenium-api\tests

REM Generate single file Allure report
echo Generating Single File Allure Report...
allure generate "%ALLURE_RESULTS%" -o "%ALLURE_REPORT%" --clean --single-file allure-report

echo Report generated at: %ALLURE_REPORT%

REM Check if Robot Framework execution succeeded
if %errorlevel% neq 0 (
    echo Test execution completed with failures.
) else (
    echo Test execution completed successfully.
)

REM Run the Python script to parse results and log to JIRA
echo Logging failed test cases to JIRA...
python .\selenium-web-pom\libraries\common\JiraIntegration.py

pause