"""
Unit tests for integration.py - SeleniumManager class
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSeleniumManager(unittest.TestCase):
    """Test cases for SeleniumManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock all the external dependencies
        self.selenium_patcher = patch('integration.webdriver')
        self.options_patcher = patch('integration.Options')
        self.moveto_patcher = patch('integration.moveTo')
        self.click_patcher = patch('integration.click')
        
        self.mock_webdriver = self.selenium_patcher.start()
        self.mock_options = self.options_patcher.start()
        self.mock_moveto = self.moveto_patcher.start()
        self.mock_click = self.click_patcher.start()
        
        # Mock Chrome driver
        self.mock_chrome_driver = Mock()
        self.mock_webdriver.Chrome.return_value = self.mock_chrome_driver
        
        # Mock Chrome options
        self.mock_chrome_options = Mock()
        self.mock_options.return_value = self.mock_chrome_options
        
        # Now import the class after mocking
        from integration import SeleniumManager
        self.selenium_manager = SeleniumManager()
    
    def tearDown(self):
        """Clean up patches"""
        self.selenium_patcher.stop()
        self.options_patcher.stop()
        self.moveto_patcher.stop()
        self.click_patcher.stop()
    
    def test_initialize_webdriver(self):
        """Test Initialze_webdriver method"""
        self.selenium_manager.Initialze_webdriver()
        
        # Verify Chrome options were configured correctly
        self.mock_chrome_options.add_experimental_option.assert_any_call("useAutomationExtension", False)
        self.mock_chrome_options.add_experimental_option.assert_any_call("excludeSwitches", ["enable-automation"])
        self.mock_chrome_options.add_argument.assert_any_call("--disable-blink-features=AutomationControlled")
        self.mock_chrome_options.add_argument.assert_any_call("user-data-dir=C:/Users/AM/AppData/Local/Google/Chrome/User Data")
        self.mock_chrome_options.add_argument.assert_any_call("profile-directory=Profile 4")
        
        # Verify Chrome driver was created with options
        self.mock_webdriver.Chrome.assert_called_once_with(options=self.mock_chrome_options)
        
        # Verify window was maximized
        self.mock_chrome_driver.maximize_window.assert_called_once()
    
    def test_get_webdriver(self):
        """Test get_webdriver method"""
        self.selenium_manager.Initialze_webdriver()
        driver = self.selenium_manager.get_webdriver()
        
        self.assertEqual(driver, self.mock_chrome_driver)
    
    def test_get_webdriver_before_initialization(self):
        """Test get_webdriver method before initialization"""
        # Should return None if not initialized
        driver = self.selenium_manager.get_webdriver()
        self.assertIsNone(driver)
    
    def test_navigate_to_elem(self):
        """Test navigate_to_elem method"""
        # Initialize webdriver first
        self.selenium_manager.Initialze_webdriver()
        
        # Mock window position and size
        self.mock_chrome_driver.get_window_position.return_value = {'x': 100, 'y': 50}
        self.mock_chrome_driver.execute_script.side_effect = [
            20,  # outerHeight - innerHeight (browser_offset_y)
            10,  # outerWidth - innerWidth (browser_offset_x)
            {'left': 200, 'top': 150, 'width': 100, 'height': 50}  # getBoundingClientRect
        ]
        
        # Mock element
        mock_element = Mock()
        
        # Call the method
        self.selenium_manager.navigate_to_elem(mock_element)
        
        # Verify window position was retrieved
        self.mock_chrome_driver.get_window_position.assert_called_once()
        
        # Verify execute_script was called for offsets and element rect
        expected_calls = [
            unittest.mock.call("return window.outerHeight - window.innerHeight;"),
            unittest.mock.call("return window.outerWidth - window.innerWidth;"),
            unittest.mock.call("return arguments[0].getBoundingClientRect();", mock_element)
        ]
        self.mock_chrome_driver.execute_script.assert_has_calls(expected_calls)
        
        # Calculate expected coordinates
        # center_x = 200 + 100/2 = 250
        # center_y = 150 + 50/2 = 175
        # absolute_x = 100 + 250 + 10/2 = 355
        # absolute_y = 50 + 20 + 175 = 245
        
        # Verify moveTo was called with calculated coordinates
        self.mock_moveto.assert_called_once_with(355.0, 245.0, duration=1)
    
    def test_navigate_to_elem_with_custom_parameters(self):
        """Test navigate_to_elem with custom parameters"""
        self.selenium_manager.Initialze_webdriver()
        
        # Mock return values
        self.mock_chrome_driver.get_window_position.return_value = {'x': 0, 'y': 0}
        self.mock_chrome_driver.execute_script.side_effect = [
            0,  # browser_offset_y
            0,  # browser_offset_x
            {'left': 5, 'top': 5, 'width': 10, 'height': 10}  # Small element
        ]
        
        mock_element = Mock()
        
        # Call with custom parameters
        self.selenium_manager.navigate_to_elem(mock_element, min_coordinate=20, movement_duration=2)
        
        # center_x = 5 + 10/2 = 10
        # center_y = 5 + 10/2 = 10
        # absolute_x = 0 + 10 + 0/2 = 10, but min_coordinate=20, so 20
        # absolute_y = 0 + 0 + 10 = 10, but min_coordinate=20, so 20
        
        self.mock_moveto.assert_called_once_with(20, 20, duration=2)
    
    def test_clickOnScreen(self):
        """Test clickOnScreen method"""
        self.selenium_manager.clickOnScreen()
        
        # Verify click was called
        self.mock_click.assert_called_once()
    
    def test_navigate_to_elem_coordinate_bounds(self):
        """Test navigate_to_elem respects minimum coordinate bounds"""
        self.selenium_manager.Initialze_webdriver()
        
        # Setup to generate coordinates below minimum
        self.mock_chrome_driver.get_window_position.return_value = {'x': 0, 'y': 0}
        self.mock_chrome_driver.execute_script.side_effect = [
            0,  # browser_offset_y
            0,  # browser_offset_x
            {'left': 0, 'top': 0, 'width': 2, 'height': 2}  # Very small element
        ]
        
        mock_element = Mock()
        
        # Call with default min_coordinate=10
        self.selenium_manager.navigate_to_elem(mock_element)
        
        # Should use minimum coordinates (10, 10) instead of calculated (1, 1)
        self.mock_moveto.assert_called_once_with(10, 10, duration=1)


if __name__ == '__main__':
    unittest.main()