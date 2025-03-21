from time import sleep
from selenium.webdriver.common.by import By
from integration import SeleniumManager
from selenium.webdriver.chrome.webdriver import WebDriver


class AuthenticationManager:
    __wdriver: WebDriver = None
    __driverManager: SeleniumManager = None
    __username: str = ""
    __password: str = ""
    __input_email: list = None
    __input_pass = None
    __login_button = None
    __login_url = "https://www.facebook.com/login/"

    def __init__(
        self, driverManager: SeleniumManager, username: str, password: str
    ) -> None:
        self.__wdriver = driverManager.get_webdriver()
        self.__driverManager = driverManager
        print(type(self.__wdriver))
        self.__username = username
        self.__password = password

    def open_login_page(self):
        self.__wdriver.get(self.__login_url)
        sleep(10)

    def detect_login_page(self) -> bool:

        self.__input_email = self.__wdriver.find_element(By.NAME, "email")
        self.__input_pass = self.__wdriver.find_element(By.NAME, "pass")
        self.__login_button = self.__wdriver.find_element(By.NAME, "login")

        if self.__input_email and self.__input_pass:
            return True
        else:
            return False

    def preform_login(self) -> bool:

        self.__input_email.send_keys("  ")
        self.__input_pass.send_keys("   ")
        self.__input_email.clear()
        self.__input_pass.clear()
        self.__driverManager.navigate_to_elem(self.__input_email)
        self.__driverManager.clickOnScreen()
        self.__input_email.send_keys(self.__username)
        sleep(1)
        self.__driverManager.clickOnScreen()
        self.__driverManager.navigate_to_elem(self.__input_email)
        self.__driverManager.navigate_to_elem(self.__login_button)
        self.__input_pass.send_keys(self.__password)
        sleep(1)
        self.__driverManager.clickOnScreen()
