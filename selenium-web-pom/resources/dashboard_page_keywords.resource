*** Settings ***
Library    ../libraries/pages/DashboardPage.py

*** Keywords ***
Click "${option}" In Quick Launch

    Click Option In Quick Launch  ${option}

Click "${option}" In Menu

    Click Option In Menu  ${option}


