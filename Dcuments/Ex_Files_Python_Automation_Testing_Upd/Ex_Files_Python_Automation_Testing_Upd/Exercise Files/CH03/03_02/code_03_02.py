from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

driver= webdriver.Firefox()
driver.get("file:///C:/Users/OBT/Downloads/Ex_Files_Python_Automation_Testing_Upd/Ex_Files_Python_Automation_Testing_Upd/Exercise%20Files/CH03/03_02/html_code_03_02.html")

select= Select(driver.find_element(By.NAME, 'numReturnSelect'))
select.select_by_index(4)
time.sleep(4)
select.select_by_visible_text("200")
time.sleep(4)
select.select_by_value("250")
time.sleep(4)

options = select.options
for option in options:
    print(option.text)

submit_button = driver.find_element(By.NAME,'continue')
submit_button.submit();
time.sleep(2)

driver.close()
