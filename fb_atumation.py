from time import sleep
from auth import AuthenticationManager
from selenium import webdriver
from integration import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from config import DataManager


class ApplicationController:
    pass


# abdalrahman_magrabe@hotmail.com
# 11366699987654321
driverManager = SeleniumManager()
driverManager.Initialze_webdriver()
webdriver = driverManager.get_webdriver()
username = "maghrbi006@hotmail.com"
password = "Maghrbi##007"
authMang = AuthenticationManager(driverManager, username, password)
dataMgr = DataManager()


try:
    authMang.open_login_page()
    if authMang.detect_login_page():
        authMang.preform_login()
except Exception as e:
    print(f"An error occurred: {e}")


current_account: WebElement = webdriver.find_element(By.XPATH, dataMgr.account_name)
print(f"The name of the account is : {current_account.text}")
accountIcon: WebElement = webdriver.find_element(By.XPATH, dataMgr.account_icon).click()
sleep(2)
# driverManager.navigate_to_elem(accountIcon)
accountIcon: WebElement = webdriver.find_element(
    By.XPATH, dataMgr.all_profiles_button
).click()
sleep(1)
# driverManager.navigate_to_elem(accountIcon)
# driverManager.clickOnScreen()

accountPages = webdriver.find_elements(By.XPATH, dataMgr.pages_containter)

print(f"accounts found is : {accountPages}")
for item in accountPages:
    if len(item.text) > 0:
        print(item.text)
        driverManager.navigate_to_elem(item)

sleep(1000)
