from time import sleep
from selenium.webdriver.common.by import By
from integration import SeleniumManager
from selenium.webdriver.chrome.webdriver import WebDriver


class AuthenticationManager:
    """
    Manages login authentication using Selenium WebDriver.
    """
    __wdriver: WebDriver = None         # WebDriver instance
    __driverManager: SeleniumManager = None  # SeleniumManager instance
    __username: str = ""                # Username for login
    __password: str = ""                # Password for login
    __input_email = None                # Email input WebElement
    __input_pass = None                 # Password input WebElement
    __login_button = None               # Login button WebElement
    __login_url: str = "https://www.facebook.com/login/"  # Login page URL

    def __init__(self, driverManager: SeleniumManager, username: str, password: str) -> None:
        """
        Initializes the AuthenticationManager with a SeleniumManager instance, username, and password.
        
        :param driverManager: Provides the WebDriver instance.
        :param username: Username for authentication.
        :param password: Password for authentication.
        """
        self.__wdriver = driverManager.get_webdriver()  # Retrieve the WebDriver
        self.__driverManager = driverManager              # Store SeleniumManager
        self.__username = username                        # Store username
        self.__password = password                        # Store password
        print(f"[DEBUG] WebDriver type: {type(self.__wdriver)}")  # Debug: print WebDriver's type

    def open_login_page(self) -> None:
        """
        Opens the Facebook login page and waits for it to load.
        """
        try:
            print("[DEBUG] Opening login page...")
            self.__wdriver.get(self.__login_url)
            sleep(10)  # Consider replacing sleep with an explicit wait for better stability
            print("[DEBUG] Login page opened successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to open login page: {e}")

    def detect_login_page(self) -> bool:
        """
        Detects if the essential login elements are present.
        
        :return: True if email, password, and login button elements are found; otherwise, False.
        """
        try:
            print("[DEBUG] Detecting login page elements...")
            self.__input_email = self.__wdriver.find_element(By.NAME, "email")
            self.__input_pass = self.__wdriver.find_element(By.NAME, "pass")
            self.__login_button = self.__wdriver.find_element(By.NAME, "login")
            print("[DEBUG] Login page elements detected successfully.")
            return self.__input_email is not None and self.__input_pass is not None
        except Exception as e:
            print(f"[ERROR] detect_login_page error: {e}")
            return False

    def _clear_fields(self) -> None:
        """
        Clears any pre–filled data in the login fields.
        """
        # Send dummy keys then clear to ensure fields are blank.
        self.__input_email.send_keys("  ")
        self.__input_pass.send_keys("   ")
        self.__input_email.clear()
        self.__input_pass.clear()

    def preform_login(self) -> bool:
        """
        Performs the login process by simulating user interactions.
        
        :return: True if login steps are executed successfully; otherwise, False.
        """
        try:
            print("[DEBUG] Performing login...")
            self._clear_fields()  # Clear any existing content

            # Navigate to email field and simulate user entering the username.
            self.__driverManager.navigate_to_elem(self.__input_email)
            self.__driverManager.clickOnScreen()
            self.__input_email.send_keys(self.__username)
            sleep(1)  # Replace with an explicit wait if possible

            # Simulate an extra screen click (if needed to register input).
            self.__driverManager.clickOnScreen()

            # Navigate to the login button (or password field), then enter the password.
            self.__driverManager.navigate_to_elem(self.__login_button)
            self.__input_pass.send_keys(self.__password)
            sleep(1)  # Replace with an explicit wait

            # Final click to submit the login form.
            self.__driverManager.clickOnScreen()
            print("[DEBUG] Login performed successfully.")
            return True
        except Exception as e:
            print(f"[ERROR] preform_login error: {e}")
            return False
