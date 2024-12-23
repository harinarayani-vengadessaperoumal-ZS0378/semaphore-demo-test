from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get("https://www.google.com/")
driver.implicitly_wait(3)
driver.maximize_window()
input_element :WebElement = driver.find_element(By.ID, 'APjFqb')
input_element.click()
input_element.send_keys("Yahoo login")
entered_value = input_element.get_property("value")
print(f'Entered value is : {entered_value}')

search_button : WebElement = driver.find_element(By.NAME, 'btnK')
search_button.send_keys(Keys.ENTER)
time.sleep(3)
#driver.execute_script('window.scrollTo(0,window.innerHeight);')
driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
time.sleep(3)

actions = ActionChains(driver)
driver.close()