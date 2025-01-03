import os
from pathlib import Path

current_dir = Path(os.getcwd())

#TestData paths

exceldata_path = os.path.join(current_dir,"selenium-web-pom","data","test_data","test_data.xlsx")
login_jsondata_path = os.path.join(current_dir,"selenium-web-pom","data","test_data","login.json")
employee_jsondata_path = os.path.join(current_dir,"selenium-web-pom","data","test_data","login.json")