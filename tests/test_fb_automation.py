"""
Unit tests for fb_atumation.py - ApplicationController class
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestApplicationController(unittest.TestCase):
    """Test cases for ApplicationController class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock all dependencies
        self.selenium_manager_patcher = patch('fb_atumation.SeleniumManager')
        self.auth_manager_patcher = patch('fb_atumation.AuthenticationManager')
        self.data_manager_patcher = patch('fb_atumation.DataManager')
        self.config_manager_patcher = patch('fb_atumation.ConfigManager')
        self.sleep_patcher = patch('fb_atumation.sleep')
        
        self.mock_selenium_manager_class = self.selenium_manager_patcher.start()
        self.mock_auth_manager_class = self.auth_manager_patcher.start()
        self.mock_data_manager_class = self.data_manager_patcher.start()
        self.mock_config_manager_class = self.config_manager_patcher.start()
        self.mock_sleep = self.sleep_patcher.start()
        
        # Setup mock instances
        self.mock_selenium_manager = Mock()
        self.mock_webdriver = Mock()
        self.mock_auth_manager = Mock()
        self.mock_data_manager = Mock()
        self.mock_config_manager = Mock()
        
        # Configure mocks
        self.mock_selenium_manager_class.return_value = self.mock_selenium_manager
        self.mock_selenium_manager.get_webdriver.return_value = self.mock_webdriver
        self.mock_auth_manager_class.return_value = self.mock_auth_manager
        self.mock_data_manager_class.return_value = self.mock_data_manager
        self.mock_config_manager_class.return_value = self.mock_config_manager
        
        # Setup data manager attributes
        self.mock_data_manager.account_name = "//span[@class='account-name']"
        self.mock_data_manager.account_icon = "//div[@class='account-icon']"
        self.mock_data_manager.all_profiles_button = "//button[@class='profiles']"
        self.mock_data_manager.pages_containter = "//div[@class='pages-container']"
        
        # Import and create ApplicationController
        from fb_atumation import ApplicationController
        self.app_controller = ApplicationController()
    
    def tearDown(self):
        """Clean up patches"""
        self.selenium_manager_patcher.stop()
        self.auth_manager_patcher.stop()
        self.data_manager_patcher.stop()
        self.config_manager_patcher.stop()
        self.sleep_patcher.stop()
    
    def test_initialization(self):
        """Test ApplicationController initialization"""
        # Verify SeleniumManager was created and initialized
        self.mock_selenium_manager_class.assert_called_once()
        self.mock_selenium_manager.Initialze_webdriver.assert_called_once()
        self.mock_selenium_manager.get_webdriver.assert_called_once()
        
        # Verify managers were created
        self.mock_auth_manager_class.assert_called_once_with(
            self.mock_selenium_manager, 
            "maghrbi006@hotmail.com", 
            "Maghrbi##007"
        )
        self.mock_data_manager_class.assert_called_once()
        self.mock_config_manager_class.assert_called_once()
        
        # Verify instance attributes
        self.assertEqual(self.app_controller.driverManager, self.mock_selenium_manager)
        self.assertEqual(self.app_controller.webdriver, self.mock_webdriver)
        self.assertEqual(self.app_controller.username, "maghrbi006@hotmail.com")
        self.assertEqual(self.app_controller.password, "Maghrbi##007")
        self.assertEqual(self.app_controller.authMang, self.mock_auth_manager)
        self.assertEqual(self.app_controller.dataMgr, self.mock_data_manager)
        self.assertEqual(self.app_controller.confgMgr, self.mock_config_manager)
    
    def test_login_success(self):
        """Test login method when successful"""
        # Setup mocks for successful login
        self.mock_auth_manager.detect_login_page.return_value = True
        self.mock_auth_manager.preform_login.return_value = True
        
        result = self.app_controller.login()
        
        # Verify login flow
        self.mock_auth_manager.open_login_page.assert_called_once()
        self.mock_auth_manager.detect_login_page.assert_called_once()
        self.mock_auth_manager.preform_login.assert_called_once()
        
        self.assertTrue(result)
    
    def test_login_detect_page_failure(self):
        """Test login method when detect_login_page fails"""
        # Setup mocks for detect page failure
        self.mock_auth_manager.detect_login_page.return_value = False
        
        result = self.app_controller.login()
        
        # Verify login flow stops at detect_login_page
        self.mock_auth_manager.open_login_page.assert_called_once()
        self.mock_auth_manager.detect_login_page.assert_called_once()
        self.mock_auth_manager.preform_login.assert_not_called()
        
        self.assertTrue(result)  # Method still returns True if detect fails
    
    def test_login_exception_handling(self):
        """Test login method exception handling"""
        # Setup mock to raise exception
        self.mock_auth_manager.open_login_page.side_effect = Exception("Network error")
        
        result = self.app_controller.login()
        
        # Verify exception is caught and False is returned
        self.assertFalse(result)
    
    def test_setup_account_ui_success(self):
        """Test setup_account_ui method when successful"""
        # Setup mock elements
        mock_account_element = Mock()
        mock_account_element.text = "Test Account Name"
        mock_icon_element = Mock()
        mock_button_element = Mock()
        
        self.mock_webdriver.find_element.side_effect = [
            mock_account_element,
            mock_icon_element,
            mock_button_element
        ]
        
        self.app_controller.setup_account_ui()
        
        # Verify elements were found and clicked
        expected_calls = [
            unittest.mock.call(unittest.mock.ANY, self.mock_data_manager.account_name),
            unittest.mock.call(unittest.mock.ANY, self.mock_data_manager.account_icon),
            unittest.mock.call(unittest.mock.ANY, self.mock_data_manager.all_profiles_button)
        ]
        self.mock_webdriver.find_element.assert_has_calls(expected_calls)
        
        # Verify clicks
        mock_icon_element.click.assert_called_once()
        mock_button_element.click.assert_called_once()
        
        # Verify account name was set in config manager
        self.assertEqual(self.mock_config_manager.currentAccount, "Test Account Name")
        
        # Verify sleep calls
        self.assertEqual(self.mock_sleep.call_count, 2)
        self.mock_sleep.assert_any_call(2)
        self.mock_sleep.assert_any_call(1)
    
    def test_setup_account_ui_exception_handling(self):
        """Test setup_account_ui method exception handling"""
        # Setup mock to raise exception
        self.mock_webdriver.find_element.side_effect = Exception("Element not found")
        
        # Should not raise exception
        self.app_controller.setup_account_ui()
        
        # Verify find_element was called (and failed)
        self.mock_webdriver.find_element.assert_called()
    
    def test_retrieve_account_pages_success(self):
        """Test retrieve_account_pages method when successful"""
        # Setup mock container element
        mock_container = Mock()
        mock_pages = [Mock(), Mock()]
        
        self.mock_webdriver.find_element.return_value = mock_container
        self.mock_config_manager.getAccountPages.return_value = mock_pages
        
        self.app_controller.retrieve_account_pages()
        
        # Verify container was found
        self.mock_webdriver.find_element.assert_called_once_with(
            unittest.mock.ANY, self.mock_data_manager.pages_containter
        )
        
        # Verify container was set in config manager
        self.assertEqual(self.mock_config_manager.PagesOnAccount, mock_container)
        
        # Verify account pages were retrieved
        self.mock_config_manager.getAccountPages.assert_called_once()
        
        # Verify pages were stored in data manager
        self.assertEqual(self.mock_data_manager.account_pages, mock_pages)
    
    def test_retrieve_account_pages_exception_handling(self):
        """Test retrieve_account_pages method exception handling"""
        # Setup mock to raise exception
        self.mock_webdriver.find_element.side_effect = Exception("Container not found")
        
        # Should not raise exception
        self.app_controller.retrieve_account_pages()
        
        # Verify find_element was called (and failed)
        self.mock_webdriver.find_element.assert_called()
    
    def test_run_method_success_flow(self):
        """Test run method with successful flow"""
        # Setup mocks for successful flow
        self.mock_auth_manager.detect_login_page.return_value = True
        self.mock_auth_manager.preform_login.return_value = True
        
        # Mock elements for setup_account_ui
        mock_account_element = Mock()
        mock_account_element.text = "Test Account"
        mock_icon_element = Mock()
        mock_button_element = Mock()
        mock_container = Mock()
        
        self.mock_webdriver.find_element.side_effect = [
            mock_account_element,  # account_name
            mock_icon_element,     # account_icon  
            mock_button_element,   # all_profiles_button
            mock_container         # pages_containter
        ]
        
        self.app_controller.run()
        
        # Verify complete flow was executed
        self.mock_auth_manager.open_login_page.assert_called_once()
        self.mock_auth_manager.detect_login_page.assert_called_once()
        self.mock_auth_manager.preform_login.assert_called_once()
        
        # Verify UI setup was called
        mock_icon_element.click.assert_called_once()
        mock_button_element.click.assert_called_once()
        
        # Verify pages retrieval was called
        self.mock_config_manager.getAccountPages.assert_called_once()
        
        # Verify final sleep (debugging sleep)
        self.mock_sleep.assert_any_call(1000)
    
    def test_run_method_login_failure(self):
        """Test run method when login fails"""
        # Setup login to fail
        self.mock_auth_manager.open_login_page.side_effect = Exception("Login failed")
        
        self.app_controller.run()
        
        # Verify method returns early on login failure
        self.mock_auth_manager.open_login_page.assert_called_once()
        
        # Verify subsequent methods are not called
        self.mock_webdriver.find_element.assert_not_called()
        self.mock_config_manager.getAccountPages.assert_not_called()
    
    def test_credentials_are_set_correctly(self):
        """Test that credentials are set correctly in initialization"""
        self.assertEqual(self.app_controller.username, "maghrbi006@hotmail.com")
        self.assertEqual(self.app_controller.password, "Maghrbi##007")
        
        # Verify credentials were passed to AuthenticationManager
        self.mock_auth_manager_class.assert_called_once_with(
            self.mock_selenium_manager,
            "maghrbi006@hotmail.com",
            "Maghrbi##007"
        )


if __name__ == '__main__':
    unittest.main()