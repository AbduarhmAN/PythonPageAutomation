from time import sleep
from auth import AuthenticationManager
from integration import SeleniumManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from config import DataManager, ConfigManager
from env_config import env_config
from validation import validate_automation_inputs
from xpath_config import SelectorManager
from cleanup import CleanupManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ApplicationController:
    """
    A controller class to encapsulate the flow:
        - Initialize WebDriver and managers.
        - Perform login.
        - Navigate account UI.
        - Retrieve pages container and filter pages.
    """
    def __init__(self):
        """Initialize the application with environment-based configuration."""
        logger.info("Initializing ApplicationController...")
        
        # Validate configuration
        if not env_config.validate_config():
            raise ValueError("Invalid configuration. Please check your .env file.")
        
        if env_config.debug_mode:
            env_config.print_config_summary()
        
        # Get credentials from environment configuration
        self.username = env_config.fb_username
        self.password = env_config.fb_password
        
        # Validate credentials
        if not validate_automation_inputs(self.username, self.password, 
                                        env_config.chrome_user_data_dir, 
                                        env_config.chrome_profile_dir):
            raise ValueError("Invalid automation inputs. Please check your credentials and configuration.")
        
        logger.info(f"Configured for user: {self.username[:3]}***@{self.username.split('@')[1] if '@' in self.username else 'unknown'}")

        # Initialize the driver manager and get the webdriver.
        self.driverManager = SeleniumManager()
        self.driverManager.initialize_webdriver()
        self.webdriver = self.driverManager.get_webdriver()

        # Initialize managers.
        self.authMang = AuthenticationManager(self.driverManager, self.username, self.password)
        self.dataMgr = DataManager()
        self.confgMgr = ConfigManager()
        self.selector_manager = SelectorManager(self.webdriver)
        self.cleanup_manager = CleanupManager(self.webdriver)

    def login(self):
        """
        Executes the login sequence using AuthenticationManager.
        """
        logger.info("Starting login process...")
        try:
            self.authMang.open_login_page()
            if self.authMang.detect_login_page():
                success = self.authMang.perform_login()
                if success:
                    logger.info("Login completed successfully")
                else:
                    logger.error("Login failed")
                return success
            else:
                logger.error("Login page not detected properly")
                return False
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def setup_account_ui(self):
        """
        Performs the necessary UI actions to reveal the account pages container.
        """
        logger.info("Setting up account UI...")
        try:
            # Retrieve current account using improved selector
            current_account_elem: WebElement = self.selector_manager.get_account_name_element()
            if not current_account_elem:
                raise Exception("Account name element not found")
                
            self.confgMgr.currentAccount = current_account_elem.text
            logger.info(f"Account name: {self.confgMgr.currentAccount}")

            # Click the account icon using improved selector
            account_icon = self.selector_manager.get_account_icon_element()
            if not account_icon:
                raise Exception("Account icon element not found")
            
            account_icon.click()
            sleep(2)  # TODO: Replace with explicit wait
            
            # Click the all profiles button using improved selector
            all_profiles_button = self.selector_manager.get_all_profiles_button_element()
            if not all_profiles_button:
                raise Exception("All profiles button element not found")
                
            all_profiles_button.click()
            sleep(1)  # TODO: Replace with explicit wait
            logger.info("Account UI setup completed")
        except Exception as e:
            logger.error(f"Error during UI setup: {e}")
            raise

    def retrieve_account_pages(self):
        """
        Retrieves the pages container and uses ConfigManager to filter the account pages.
        """
        logger.info("Retrieving account pages...")
        try:
            # Find container element using improved selector
            pages_container = self.selector_manager.get_pages_container_element()
            if not pages_container:
                raise Exception("Pages container element not found")
                
            self.confgMgr.PagesOnAccount = pages_container
            self.dataMgr.account_pages = self.confgMgr.getAccountPages()
            logger.info("Account pages retrieved successfully.")
        except Exception as e:
            logger.error(f"Error retrieving account pages: {e}")
            raise

    def run(self):
        """
        Executes the complete automation flow.
        """
        logger.info("Starting automation flow...")
        try:
            if not self.login():
                logger.error("Login failed, aborting automation")
                return False
            
            self.setup_account_ui()
            self.retrieve_account_pages()
            
            logger.info("Automation flow completed successfully")
            # For debugging purposes. In production, use explicit waits.
            if env_config.debug_mode:
                logger.info("Debug mode: keeping browser open for 30 seconds")
                sleep(30)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in automation flow: {e}")
            return False
        finally:
            # Clean up resources
            logger.info("Performing cleanup...")
            cleanup_results = self.cleanup_manager.complete_cleanup()
            if all(cleanup_results.values()):
                logger.info("Cleanup completed successfully")
            else:
                logger.warning(f"Some cleanup tasks failed: {cleanup_results}")


def main():
    """Main entry point for the application."""
    try:
        app_controller = ApplicationController()
        success = app_controller.run()
        exit_code = 0 if success else 1
        logger.info(f"Application exiting with code: {exit_code}")
        return exit_code
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
