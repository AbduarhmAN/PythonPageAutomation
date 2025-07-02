from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from integration import SeleniumManager
from selenium.webdriver.chrome.webdriver import WebDriver
from env_config import env_config
import logging

logger = logging.getLogger(__name__)


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
    __login_url: str = None  # Login page URL (loaded from config)

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
        self.__login_url = env_config.fb_login_url       # Get login URL from config
        self.__wait = WebDriverWait(self.__wdriver, 10)   # Initialize WebDriver wait
        
        if env_config.debug_mode:
            logger.debug(f"WebDriver type: {type(self.__wdriver)}")

    def open_login_page(self) -> None:
        """
        Opens the Facebook login page and waits for it to load.
        """
        logger.info(f"Opening login page: {self.__login_url}")
        self.__wdriver.get(self.__login_url)
        
        # Use explicit wait instead of sleep
        try:
            self.__wait.until(EC.presence_of_element_located((By.NAME, "email")))
            logger.info("Login page loaded successfully")
        except Exception as e:
            logger.warning(f"Timeout waiting for login page, proceeding anyway: {e}")
            sleep(5)  # Fallback sleep

    def detect_login_page(self) -> bool:
        """
        Detects if the essential login elements are present.
        
        :return: True if email, password, and login button elements are found; otherwise, False.
        """
        try:
            # Use explicit waits to locate required elements
            self.__input_email = self.__wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            self.__input_pass = self.__wdriver.find_element(By.NAME, "pass")
            self.__login_button = self.__wdriver.find_element(By.NAME, "login")
            
            logger.info("Login page elements detected successfully")
            return self.__input_email is not None and self.__input_pass is not None
        except Exception as e:
            logger.error(f"detect_login_page error: {e}")
            return False

    def _clear_fields(self) -> None:
        """
        Clears any pre-filled data in the login fields.
        """
        try:
            # Clear fields using Selenium's clear method
            self.__input_email.clear()
            self.__input_pass.clear()
            logger.debug("Login fields cleared")
        except Exception as e:
            logger.warning(f"Error clearing fields: {e}")

    def perform_login(self) -> bool:
        """
        Performs the login process by simulating user interactions.
        
        :return: True if login steps are executed successfully; otherwise, False.
        """
        try:
            logger.info("Starting login process...")
            self._clear_fields()  # Clear any existing content

            # Navigate to email field and simulate user entering the username.
            self.__driverManager.navigate_to_elem(self.__input_email)
            self.__driverManager.clickOnScreen()
            self.__input_email.send_keys(self.__username)
            
            # Use explicit wait instead of sleep
            try:
                self.__wait.until(lambda driver: self.__input_email.get_attribute("value") != "")
            except:
                sleep(1)  # Fallback

            # Simulate an extra screen click (if needed to register input).
            self.__driverManager.clickOnScreen()

            # Navigate to the login button (or password field), then enter the password.
            self.__driverManager.navigate_to_elem(self.__login_button)
            self.__input_pass.send_keys(self.__password)
            
            # Use explicit wait
            try:
                self.__wait.until(lambda driver: self.__input_pass.get_attribute("value") != "")
            except:
                sleep(1)  # Fallback

            # Final click to submit the login form.
            self.__driverManager.clickOnScreen()
            
            # Wait for page to change after login
            try:
                self.__wait.until(lambda driver: driver.current_url != self.__login_url)
                logger.info("Login form submitted successfully")
            except:
                logger.warning("Login submission timeout, but proceeding")
                sleep(3)  # Fallback
            
            return True
        except Exception as e:
            logger.error(f"perform_login error: {e}")
            return False
