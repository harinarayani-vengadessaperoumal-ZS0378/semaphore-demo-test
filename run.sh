#!/bin/bash

# Set the number of parallel processes
PROCESSES=1

# Specify the tags you want to include and exclude
INCLUDE_TAGS="SmokeORTC_001"
EXCLUDE_TAGS="Disabled"

# Accept browser name as a parameter or default to chrome
BROWSER=${1:-chrome}

# Default to 'head' mode if no argument is passed
MODE=${2:-head}

# Set single Allure results directory for all tests
ALLURE_RESULTS="./output/allure-results"
ALLURE_REPORT="./output/allure-report"

# Create Allure results directory if it doesn't exist
mkdir -p "$ALLURE_RESULTS"
mkdir -p "$ALLURE_REPORT"

# Run web tests with Allure reporting
echo "Running Web Tests..."
pabot --processes $PROCESSES \
      --testlevelsplit \
      --variable "browser:$BROWSER" \
      --variable "mode:$MODE" \
      --pythonpath ./selenium-web-pom \
      --outputdir ./selenium-web-pom/test-results \
      --include "$INCLUDE_TAGS" \
      --exclude "$EXCLUDE_TAGS" \
      --listener "allure_robotframework:$ALLURE_RESULTS" \
      ./selenium-web-pom/tests

# Run API tests with Allure reporting
echo "Running API Tests..."
pabot --processes $PROCESSES \
      --testlevelsplit \
      --pythonpath ./selenium-api \
      --outputdir ./selenium-api/test-results \
      --include "$INCLUDE_TAGS" \
      --listener "allure_robotframework:$ALLURE_RESULTS" \
      ./selenium-api/tests

# Generate single file Allure report
echo "Generating Single File Allure Report..."
allure generate "$ALLURE_RESULTS" -o "$ALLURE_REPORT" --clean --single-file allure-report

echo "Report generated at: $ALLURE_REPORT"

# Check if Robot Framework execution succeeded
if [ $? -ne 0 ]; then
    echo "Test execution completed with failures."
else
    echo "Test execution completed successfully."
fi

# Run the Python script to parse results and log to JIRA
echo "Logging failed test cases to JIRA..."
python ./selenium-web-pom/libraries/common/JiraIntegration.py