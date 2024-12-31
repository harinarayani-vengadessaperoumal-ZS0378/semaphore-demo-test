from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from libraries.common.Utils import Utils
import yaml
import os
import json
import logging
import os
import sys
from allure_commons.types import AttachmentType
from pathlib import Path
import shutil
import AllureLibrary
from datetime import datetime
from libraries.common.Drivers import drivers
from selenium.webdriver.chrome.service import Service
import re

class Setup:
    """Setup Class for WebDriver initialization and logging configuration."""
    def __init__(self):
        self.current_browser = None
        self.logs_dir = Path(os.getcwd()) / "test_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.builtin = BuiltIn()
        self.network_logs = []
        self.test_start_time = None
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    @keyword("Clear Previous Run Results")
    def clear_previous_run_results(self, browser:str=None, environment:str=None, clear_report_web:bool=True):
        """Clears the previous run results before starting the test"""
        if(clear_report_web):
            self.clear_previous_execution_reports("output","allure")
            self.clear_previous_execution_reports("test_logs")
        environment = self.retrieve_environment_variable("ENVIRONMENT")
        self.set_environment_properties(browser, environment)

    
    @keyword("Get Configuration for the test")
    def get_config_value(self, key):
        '''This method retrieves the values from YAML Config file'''
        current_dir = Path(os.getcwd())
        execution_environment = os.getenv('ENVIRONMENT', BuiltIn().get_variable_value("${environment}")) 
        #file_path = f'{current_dir}\\selenium-web-pom\\data\\{execution_environment}\\web_config.yaml'
        file_path = os.path.join(current_dir,"selenium-web-pom","data",execution_environment,"web_config.yaml")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The config file at '{file_path}' was not found.")
        
        try:
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
        except Exception as e:
            raise Exception(f"Error reading the config file: {e}")
        
        if key not in config:
            raise KeyError(f"The key '{key}' was not found in the configuration.")

        return config.get(key, None)
    
    @keyword("Init Setup And Launch Browser")
    def init_setup_and_launch_browser(self, browser):
        """Read browser and environment values, configure capabilities, and launch browser."""
        website = self.retrieve_environment_variable("BASE_URL")
        self.current_browser = browser
        options = None
        driver = None
        self.network_logs = []
        self.test_start_time = datetime.now()
        mode = self.retrieve_environment_variable("MODE")
        
        if browser == "chrome":
            options = ChromeOptions()
            if mode == "headless":
                options.add_argument("--headless=new")  # For headless execution
                options.add_argument("--disable-gpu")   # Recommended for headless mode
                print('Chrome Browser is running in headless mode.')
            else:
                print('Chrome Browser is running in head mode.')
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-extensions")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            options.set_capability('goog:loggingPrefs', {
                'browser': 'ALL',
                'performance': 'ALL',
                'network': 'ALL'
            })
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option("prefs", prefs)

            driver_version = "131.0.6778.70" #added this variable for jenkin execution
            driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version).install()), options=options) #this used for jenkins execution
            
        elif browser == "firefox":
            fp = webdriver.FirefoxProfile()
            
            fp.set_preference("dom.disable_open_during_load", True)
            fp.set_preference("extensions.enabled", False)
            fp.set_preference("devtools.console.stdout.content", True)
            fp.set_preference("devtools.console.log.level", "all")
            
            options = FirefoxOptions()
            if mode=="headless":
                options.add_argument("--headless=new")  # For headless execution
                options.add_argument("--disable-gpu")   # Recommended for headless mode
                print('Firefox browser is running in headless mode.')
            options.profile = fp
            options.log_level = 'trace'
            
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )
            self.start_network_logging(driver, browser)
            
        elif browser == "edge":
            options = EdgeOptions()
            if mode=="headless":
                options.add_argument("--headless=new")  # For headless execution
                options.add_argument("--disable-gpu")   # Recommended for headless mode
                print('Edge browser is running in headless mode.')
            options.use_chromium = True
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-extensions")
            
            options.set_capability('ms:edgeChromium', True)
            options.set_capability('browserName', 'MicrosoftEdge')
            
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
            
            self.start_network_logging(driver, browser)

        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.maximize_window()

        # Navigate to Website
        driver.get(website)
        Utils.wait_for_page_load()

        # Set driver to Robot's SeleniumLibrary
        BuiltIn().get_library_instance('SeleniumLibrary').register_driver(driver, alias="driver")
        
        return driver

    def start_network_logging(self, driver, browser):
        """Start collecting network logs for different browsers."""
        try:
            if browser == "chrome":
                driver.get_log('performance')
                self.network_logs = []
                self.logger.info("Started Chrome network logging")
            
            elif browser == "firefox":
                try:
                    profile = driver.firefox_profile
                    profile.set_preference("devtools.console.stdout.content", True)
                    profile.set_preference("devtools.console.log.level", "all")
                    profile.set_preference("devtools.netmonitor.enabled", True)
                    profile.set_preference("devtools.netmonitor.persistent", True)
                    
                    options = FirefoxOptions()
                    options.log_level = 'trace'
                    
                    self.network_logs = []
                    self.logger.info("Configured Firefox logging")
                except Exception as firefox_log_error:
                    self.logger.warning(f"Firefox log configuration issue: {firefox_log_error}")
            
            elif browser == "edge":
                try:
                    driver.get_log('browser')
                    self.network_logs = []
                    self.logger.info("Started Edge network logging")
                except Exception as log_error:
                    self.logger.warning(f"Standard log retrieval failed. Using alternative logging: {str(log_error)}")
                    self.network_logs = []
        
        except Exception as e:
            self.logger.error(f"Failed to start network logging for {browser}: {str(e)}")

    def process_network_logs(self, driver, test_name: str) -> str:
        """
        Process and save network logs collected during test execution across browsers.
        """
        try:
            processed_logs = []
            
            if self.current_browser == "chrome":
                # Chrome performance log processing
                new_logs = driver.get_log('performance')
                for entry in new_logs:
                    try:
                        message = json.loads(entry['message'])
                        if 'message' in message and 'method' in message['message']:
                            method = message['message']['method']
                            if method.startswith('Network.'):
                                processed_logs.append({
                                    'method': method,
                                    'timestamp': entry['timestamp'],
                                    'data': message['message'].get('params', {})
                                })
                    except (json.JSONDecodeError, KeyError) as parsing_error:
                        self.logger.warning(f"Log parsing error: {parsing_error}")
            
            elif self.current_browser == "firefox":
                try:
                    new_logs = driver.get_log('browser')
                    for entry in new_logs:
                        processed_logs.append({
                            'level': entry.get('level', 'UNKNOWN'),
                            'message': entry.get('message', 'No message'),
                            'timestamp': entry.get('timestamp', 0)
                        })
                except Exception as firefox_log_error:
                    self.logger.warning(f"Firefox log retrieval error: {firefox_log_error}")
                    # Fallback log entry
                    processed_logs.append({
                        'error': f"Log retrieval failed: {str(firefox_log_error)}"
                    })
            
            elif self.current_browser == "edge":
                try:
                    new_logs = driver.get_log('browser')
                    for entry in new_logs:
                        processed_logs.append({
                            'level': entry.get('level', 'UNKNOWN'),
                            'message': entry.get('message', 'No message'),
                            'timestamp': entry.get('timestamp', 0)
                        })
                
                except Exception as log_error:
                    self.logger.warning(f"Edge log retrieval error: {str(log_error)}")
                    processed_logs.append({
                        'error': f"Log retrieval failed: {str(log_error)}"
                    })
            
            test_name = re.sub(r'[^a-zA-Z0-9_]', '_', test_name)
            log_file_path = os.path.join(self.logs_dir, f"network_logs_{test_name}.json")

            # Save all collected logs to file
            with open(log_file_path, 'w') as f:
                json.dump({
                    'test_name': test_name,
                    'browser': self.current_browser,
                    'start_time': self.test_start_time.isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'logs': processed_logs
                }, f, indent=2)
            
            return log_file_path
            
        except Exception as e:
            self.logger.error(f"Failed to process network logs for {self.current_browser}: {str(e)}")
            return None

    @keyword("Capture Network Logs On Failure")
    def capture_network_logs_on_failure(self) -> None:
        """Capture and attach network logs on test failure for all browsers."""
        try:
            test_status = self.builtin.get_variable_value("${TEST STATUS}")
            test_name = self.builtin.get_variable_value("${TEST NAME}")
            
            if test_status and test_status.upper() == "FAIL":
                driver = self.builtin.get_library_instance('SeleniumLibrary').driver
                
                # Process and attach logs for all supported browsers
                log_file_path = self.process_network_logs(driver, test_name)
                if log_file_path:
                    AllureLibrary.attach_file(
                        log_file_path,
                        name=f"{test_name}_network_logs",
                        attachment_type=AttachmentType.TEXT
                    )
                    
        except Exception as e:
            self.logger.error(f"Failed to capture logs: {str(e)}")

    

    def set_environment_properties(self, browser, environment):
        """Set environment properties in the allure-results directory"""
        try:
            env_file_path = os.path.join("output", "allure-results", "environment.properties")
            
            if not os.path.exists(os.path.dirname(env_file_path)):
                os.makedirs(os.path.dirname(env_file_path))
            
            with open(env_file_path, "w") as env_file:
                env_file.write(f"BROWSER={browser}\n")
                env_file.write(f"ENVIRONMENT={environment}\n")
                env_file.write(f"OS=Windows 11\n")
                env_file.write(f"PYTHON_VERSION=3.13.0\n")
                env_file.write(f"SELENIUM_VERSION=4.1.0\n")
                env_file.write(f"ROBOTFRAMEWORK_VERSION=4.1.3\n")
        except Exception as e:
            logging.error(f"Error setting environment properties: {str(e)}")

    @keyword("Clear previous execution reports")
    def clear_previous_execution_reports(self, folder1: str, folder2: str = None):
        """
        Clears the contents of specified folder(s).
        """
        try:
            # Construct the directory path based on whether folder2 is provided
            if folder2:
                target_dir = os.path.join(os.getcwd(), folder1, folder2)
            else:
                target_dir = os.path.join(os.getcwd(), folder1)

            # Check if the folder exists
            if os.path.exists(target_dir):
                # Remove all files and subdirectories in the target folder
                try:
                    for filename in os.listdir(target_dir):
                        file_path = os.path.join(target_dir, filename)
                        try:
                            if os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                            else:
                                os.remove(file_path)
                        except Exception as file_error:
                            self.logger.error(f"Error removing {file_path}: {str(file_error)}")
                            continue
                    
                    self.logger.info(f"Successfully cleared folder: {target_dir}")
                except Exception as clear_error:
                    self.logger.error(f"Error clearing folder {target_dir}: {str(clear_error)}")
            else:
                # Create the directory if it doesn't exist
                try:
                    os.makedirs(target_dir)
                    self.logger.info(f"Created folder: {target_dir}")
                except Exception as mkdir_error:
                    self.logger.error(f"Error creating folder {target_dir}: {str(mkdir_error)}")
                    
        except Exception as e:
            self.logger.error(f"Unexpected error in clear_previous_execution_reports: {str(e)}")

    @keyword("Close The Browser")
    def close_the_browser(self) -> None:
        """Closing the browser"""
        try:
            seleniumlib = drivers.get_selinuim_driver()
            seleniumlib.close_browser()
        except Exception as e:
            self.logger.error(f"Failed to close browser: {str(e)}")
    
    @keyword("Setting Up The Environment Variable For The Suite")
    def set_env_variables(self):
        """
        This method setup the following environment variables:
    
        -"ENVIRONMENT": Specify qa,uat or prod environment    
        -"BASE_URL": contains the web application base url     
        -"WEB_APP_USERNAME": provides web application username      
        -"WEB_APP_PASSWORD": provides web application password     
        -"WEB_APP_PRIVATE_KEY": provides web application password's private key      
        -"BROWSER": name of the web browser used in execution 	
        """
        env_vars = {
            "ENVIRONMENT": BuiltIn().get_variable_value("${environment}"),
            "BASE_URL": self.get_config_value("orangehrm_app_url"), 
            "WEB_APP_USERNAME": self.get_config_value("username"), 
            "WEB_APP_PASSWORD": self.get_config_value("password"), 
            "WEB_APP_PRIVATE_KEY": self.get_config_value("privatekey"),
            "BROWSER": BuiltIn().get_variable_value("${browser}"),
            "MODE": self.get_config_value("mode")
        }

        for var, default_value in env_vars.items():
            if var not in os.environ or os.getenv(var) is None or os.getenv(var) == "":
                os.environ[var] = default_value

    
    @keyword("Retrieve Environment Variable")
    def retrieve_environment_variable(self,env_variable):
        """
        This method retrieve the following environment variables:
        
        -"ENVIRONMENT": Specify qa,uat or prod environment  
        -"BASE_URL": contains the web application base url   
        -"WEB_APP_USERNAME": provides web application username    
        -"WEB_APP_PASSWORD": provides web application password   
        -"WEB_APP_PRIVATE_KEY": provides web application password's private key    
        -"BROWSER": name of the web browser used in execution 	
        -"MODE": to run UI tests in head/headless mode
        """
        if env_variable not in os.environ:
            raise KeyError(f"The variable '{env_variable}' was not found in the Environment Variable.")
        return os.getenv(env_variable)
