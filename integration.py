from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pyautogui import moveTo, click
from env_config import env_config
import logging
import platform

logger = logging.getLogger(__name__)


class SeleniumManager:
    __wdriver: WebDriver = None

    def initialize_webdriver(self):
        """
        Initialize Chrome WebDriver with configuration from environment.
        Uses webdriver-manager for automatic driver management.
        """
        logger.info("Initializing Chrome WebDriver...")
        
        chrome_options = Options()
        
        # Basic Chrome options for automation
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Configure headless mode if requested
        if env_config.headless_mode:
            chrome_options.add_argument("--headless")
            logger.info("Running in headless mode")
        
        # Configure user data directory if specified
        if env_config.chrome_user_data_dir:
            user_data_dir = env_config.chrome_user_data_dir
            profile_dir = env_config.chrome_profile_dir
            
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"--profile-directory={profile_dir}")
            logger.info(f"Using Chrome profile: {profile_dir} in {user_data_dir}")
        else:
            logger.info("Using default Chrome profile")
        
        # Handle cross-platform differences
        if platform.system() == "Linux":
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
        
        try:
            # Use webdriver-manager for automatic driver management
            service = Service(ChromeDriverManager().install())
            self.__wdriver = webdriver.Chrome(service=service, options=chrome_options)
            self.__wdriver.maximize_window()
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def get_webdriver(self) -> WebDriver:
        return self.__wdriver

    def navigate_to_elem(self, element, min_coordinate=10, movement_duration=1):
        """
        Navigate mouse cursor to the center of a web element.
        
        :param element: WebElement to navigate to
        :param min_coordinate: Minimum coordinate value for safety
        :param movement_duration: Duration of mouse movement animation
        """
        try:
            outer_pos = self.__wdriver.get_window_position()

            browser_offset_y = self.__wdriver.execute_script(
                "return window.outerHeight - window.innerHeight;"
            )
            browser_offset_x = self.__wdriver.execute_script(
                "return window.outerWidth - window.innerWidth;"
            )

            rect = self.__wdriver.execute_script(
                "return arguments[0].getBoundingClientRect();", element
            )

            center_x = rect["left"] + rect["width"] / 2
            center_y = rect["top"] + rect["height"] / 2

            absolute_x = outer_pos["x"] + center_x + (browser_offset_x / 2)
            absolute_y = outer_pos["y"] + browser_offset_y + center_y

            absolute_x = max(absolute_x, min_coordinate)
            absolute_y = max(absolute_y, min_coordinate)

            if env_config.debug_mode:
                logger.debug(f"Moving mouse to coordinates: ({absolute_x}, {absolute_y})")

            moveTo(absolute_x, absolute_y, duration=movement_duration)
        except Exception as e:
            logger.error(f"Error navigating to element: {e}")
            raise

    def clickOnScreen(self):
        """
        Perform a mouse click at the current cursor position.
        """
        try:
            click()
            if env_config.debug_mode:
                logger.debug("Mouse click performed")
        except Exception as e:
            logger.error(f"Error performing click: {e}")
            raise
