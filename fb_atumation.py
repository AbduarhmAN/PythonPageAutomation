from time import sleep
from auth import AuthenticationManager
from integration import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DataManager, ConfigManager
from retrieval import GroupRetrieval


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
        self.authMang = AuthenticationManager(
            self.driverManager, self.username, self.password
        )
        self.dataMgr = DataManager()
        self.confgMgr = ConfigManager(main_page="Abdurahman Maghrbi")
        self.groupsMgr = GroupRetrieval(
            self.webdriver, self.dataMgr.groups_open_button, 2
        )

    def login(self):
        """
        Executes the login sequence using AuthenticationManager.
        """
        try:
            print("[DEBUG] Starting login process...")
            self.authMang.open_login_page()
            if self.authMang.detect_login_page():
                self.authMang.preform_login()
            print("[DEBUG] Login process completed successfully.")
        except Exception as e:
            print(f"[ERROR] Error during login: {e}")
            return False
        return True

    def setup_account_ui(self):
        """
        Performs the necessary UI actions to reveal the account pages container.
        """
        try:
            # Retrieve current account and update ConfigManager.
            sleep(5)
            current_account_elem: WebElement = self.webdriver.find_element(
                By.XPATH, self.dataMgr.account_name
            )
            self.confgMgr.currentAccount = current_account_elem.text
            print(f"Account name: {self.confgMgr.currentAccount}")

            # Click the account icon and then the all profiles button.
            self.webdriver.find_element(By.XPATH, self.dataMgr.account_icon).click()
            sleep(2)
            self.webdriver.find_element(
                By.XPATH, self.dataMgr.all_profiles_button
            ).click()
            sleep(1)
        except Exception as e:
            print(f"Error during UI setup: {e}")

    def retrieve_account_pages(self):
        """
        Retrieves the pages container and uses ConfigManager to filter the account pages.
        """
        try:
            # Find container element and update configuration.
            self.confgMgr.PagesOnAccount = self.webdriver.find_element(
                By.XPATH, self.dataMgr.pages_containter
            )
            self.dataMgr.account_pages = self.confgMgr.getAccountPages()
            print("Account pages retrieved successfully.")

            # # List all account pages with numbers and click on the selected one.
            # for idx, page_element in enumerate(self.dataMgr.account_pages, start=1):
            #     page_name = page_element.text
            #     print(f"{idx}. {page_name}")

            # # # Ask the user to select a page by number.
            # # try:
            # #     selected_number = int(input("Select a page by entering its number: "))
            # #     if 1 <= selected_number <= len(self.dataMgr.account_pages):
            # #         print(f"You selected: {self.dataMgr.account_pages[selected_number - 1].text}")

            # #         # Click on the selected page element.
            # #         self.dataMgr.account_pages[selected_number - 1].click()
            # #     else:
            # #         print("Invalid selection. Please run the program again and select a valid number.")
            # # except ValueError:
            # #     print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error retrieving account pages: {e}")

    def openGroupsPage(self):
        """
        Opens the groups page.
        """
        try:
            WebDriverWait(self.webdriver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.dataMgr.menu_button))
            ).click()
            WebDriverWait(self.webdriver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.dataMgr.groups_button))
            ).click()
            WebDriverWait(self.webdriver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, self.dataMgr.see_all_groups_button)
                )
            ).click()
            print("Groups page opened successfully.")

        except Exception as e:
            print(f"Error opening groups page: {e}")

    def run(self):
        """
        Executes the complete automation flow.
        """
        try:
            print("[DEBUG] Starting application flow...")
            if not self.login():
                return
            self.setup_account_ui()
            self.retrieve_account_pages()
            self.openGroupsPage()

            original_window = self.webdriver.current_window_handle
            for new_window in self.groupsMgr.process_buttons():
                print(f"[DEBUG] Processing new window: {new_window}")
                self.webdriver.switch_to.window(new_window)
                self.groupsMgr.initPost(self.dataMgr, self.webdriver)
                if self.groupsMgr.isPostEnabledInGroup():
                    self.groupsMgr.process_post()
                # Insert external processing for the new window here:
                # For example: post_automation.process_page(self.webdriver)
                sleep(2)  # Simulated external processing time.
                self.webdriver.close()
                self.webdriver.switch_to.window(original_window)

            print("[DEBUG] Application flow completed successfully.")
        except Exception as e:
            print(f"[ERROR] Error during application flow: {e}")


if __name__ == "__main__":
    appController = ApplicationController()
    appController.run()
