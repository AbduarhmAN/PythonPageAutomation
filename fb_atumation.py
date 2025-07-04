from time import sleep
from auth import AuthenticationManager
from integration import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from config import DataManager, ConfigManager

class ApplicationController:
    """
    A controller class to encapsulate the flow:
        - Initialize WebDriver and managers.
        - Perform login.
        - Navigate account UI.
        - Retrieve pages container and filter pages.
    """
    def __init__(self):
        # Initialize the driver manager and get the webdriver.
        self.driverManager = SeleniumManager()
        self.driverManager.Initialze_webdriver()
        self.webdriver = self.driverManager.get_webdriver()

        # Set login credentials.
        # abdalrahman_magrabe@hotmail.com
        # 11366699987654321
        self.username = "maghrbi006@hotmail.com"
        self.password = "Maghrbi##007"

        # Initialize managers.
        self.authMang = AuthenticationManager(self.driverManager, self.username, self.password)
        self.dataMgr = DataManager()
        self.confgMgr = ConfigManager()

    def login(self):
        """
        Executes the login sequence using AuthenticationManager.
        """
        try:
            self.authMang.open_login_page()
            if self.authMang.detect_login_page():
                self.authMang.preform_login()
        except Exception as e:
            print(f"Error during login: {e}")
            return False
        return True

    def setup_account_ui(self):
        """
        Performs the necessary UI actions to reveal the account pages container.
        """
        try:
            # Retrieve current account and update ConfigManager.
            current_account_elem: WebElement = self.webdriver.find_element(By.XPATH, self.dataMgr.account_name)
            self.confgMgr.currentAccount = current_account_elem.text
            print(f"Account name: {self.confgMgr.currentAccount}")

            # Click the account icon and then the all profiles button.
            self.webdriver.find_element(By.XPATH, self.dataMgr.account_icon).click()
            sleep(2)
            self.webdriver.find_element(By.XPATH, self.dataMgr.all_profiles_button).click()
            sleep(1)
        except Exception as e:
            print(f"Error during UI setup: {e}")

    def retrieve_account_pages(self):
        """
        Retrieves the pages container and uses ConfigManager to filter the account pages.
        """
        try:
            # Find container element and update configuration.
            self.confgMgr.PagesOnAccount = self.webdriver.find_element(By.XPATH, self.dataMgr.pages_containter)
            self.dataMgr.account_pages = self.confgMgr.getAccountPages()
            print("Account pages retrieved successfully.")
        except Exception as e:
            print(f"Error retrieving account pages: {e}")

    def run(self):
        """
        Executes the complete automation flow.
        """
        if not self.login():
            return
        self.setup_account_ui()
        self.retrieve_account_pages()
        # For debugging purposes. In production, use explicit waits.
        sleep(1000)


if __name__ == "__main__":
    appController = ApplicationController()
    appController.run()
