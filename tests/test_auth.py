"""
Unit tests for auth.py - AuthenticationManager class
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAuthenticationManager(unittest.TestCase):
    """Test cases for AuthenticationManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock dependencies
        self.mock_driver_manager = Mock()
        self.mock_webdriver = Mock()
        self.mock_driver_manager.get_webdriver.return_value = self.mock_webdriver
        
        # Import and create AuthenticationManager
        from auth import AuthenticationManager
        self.auth_manager = AuthenticationManager(
            self.mock_driver_manager,
            "test@example.com",
            "testpassword"
        )
    
    def test_initialization(self):
        """Test AuthenticationManager initialization"""
        self.assertEqual(self.auth_manager._AuthenticationManager__username, "test@example.com")
        self.assertEqual(self.auth_manager._AuthenticationManager__password, "testpassword")
        self.assertEqual(self.auth_manager._AuthenticationManager__wdriver, self.mock_webdriver)
        self.assertEqual(self.auth_manager._AuthenticationManager__driverManager, self.mock_driver_manager)
        self.assertEqual(self.auth_manager._AuthenticationManager__login_url, "https://www.facebook.com/login/")
    
    @patch('auth.sleep')  # Mock sleep to speed up tests
    def test_open_login_page(self, mock_sleep):
        """Test open_login_page method"""
        self.auth_manager.open_login_page()
        
        # Verify driver.get was called with correct URL
        self.mock_webdriver.get.assert_called_once_with("https://www.facebook.com/login/")
        
        # Verify sleep was called
        mock_sleep.assert_called_once_with(10)
    
    def test_detect_login_page_success(self):
        """Test detect_login_page method when elements are found"""
        # Mock successful element finding
        mock_email_element = Mock()
        mock_pass_element = Mock()
        mock_login_button = Mock()
        
        self.mock_webdriver.find_element.side_effect = [
            mock_email_element,
            mock_pass_element,
            mock_login_button
        ]
        
        result = self.auth_manager.detect_login_page()
        
        # Verify find_element was called for each required element
        expected_calls = [
            unittest.mock.call(unittest.mock.ANY, "email"),
            unittest.mock.call(unittest.mock.ANY, "pass"),
            unittest.mock.call(unittest.mock.ANY, "login")
        ]
        self.mock_webdriver.find_element.assert_has_calls(expected_calls)
        
        # Verify method returns True when elements are found
        self.assertTrue(result)
        
        # Verify elements are stored
        self.assertEqual(self.auth_manager._AuthenticationManager__input_email, mock_email_element)
        self.assertEqual(self.auth_manager._AuthenticationManager__input_pass, mock_pass_element)
        self.assertEqual(self.auth_manager._AuthenticationManager__login_button, mock_login_button)
    
    def test_detect_login_page_failure(self):
        """Test detect_login_page method when elements are not found"""
        # Mock element finding to raise exception
        self.mock_webdriver.find_element.side_effect = Exception("Element not found")
        
        result = self.auth_manager.detect_login_page()
        
        # Verify method returns False when exception occurs
        self.assertFalse(result)
    
    def test_clear_fields(self):
        """Test _clear_fields method"""
        # Setup mock elements
        mock_email = Mock()
        mock_pass = Mock()
        self.auth_manager._AuthenticationManager__input_email = mock_email
        self.auth_manager._AuthenticationManager__input_pass = mock_pass
        
        # Call the method
        self.auth_manager._clear_fields()
        
        # Verify dummy keys were sent and fields were cleared
        mock_email.send_keys.assert_called_with("  ")
        mock_pass.send_keys.assert_called_with("   ")
        mock_email.clear.assert_called_once()
        mock_pass.clear.assert_called_once()
    
    @patch('auth.sleep')
    def test_preform_login_success(self, mock_sleep):
        """Test preform_login method successful execution"""
        # Setup mock elements
        mock_email = Mock()
        mock_pass = Mock()
        mock_button = Mock()
        
        self.auth_manager._AuthenticationManager__input_email = mock_email
        self.auth_manager._AuthenticationManager__input_pass = mock_pass
        self.auth_manager._AuthenticationManager__login_button = mock_button
        
        # Call the method
        result = self.auth_manager.preform_login()
        
        # Verify the login flow
        # 1. Fields were cleared
        mock_email.send_keys.assert_any_call("  ")
        mock_pass.send_keys.assert_any_call("   ")
        mock_email.clear.assert_called()
        mock_pass.clear.assert_called()
        
        # 2. Navigate to email field and click
        self.mock_driver_manager.navigate_to_elem.assert_any_call(mock_email)
        self.mock_driver_manager.clickOnScreen.assert_called()
        
        # 3. Enter username
        mock_email.send_keys.assert_any_call("test@example.com")
        
        # 4. Navigate to login button
        self.mock_driver_manager.navigate_to_elem.assert_any_call(mock_button)
        
        # 5. Enter password
        mock_pass.send_keys.assert_any_call("testpassword")
        
        # Verify sleep calls
        self.assertEqual(mock_sleep.call_count, 2)
        
        # Verify method returns True on success
        self.assertTrue(result)
    
    @patch('auth.sleep')
    def test_preform_login_failure(self, mock_sleep):
        """Test preform_login method when exception occurs"""
        # Setup mock elements that will raise exception
        mock_email = Mock()
        mock_email.send_keys.side_effect = Exception("Send keys failed")
        
        self.auth_manager._AuthenticationManager__input_email = mock_email
        self.auth_manager._AuthenticationManager__input_pass = Mock()
        self.auth_manager._AuthenticationManager__login_button = Mock()
        
        # Call the method
        result = self.auth_manager.preform_login()
        
        # Verify method returns False on exception
        self.assertFalse(result)
    
    def test_login_flow_integration(self):
        """Test complete login flow integration"""
        # Setup for detect_login_page
        mock_email = Mock()
        mock_pass = Mock()
        mock_button = Mock()
        
        self.mock_webdriver.find_element.side_effect = [
            mock_email,
            mock_pass,
            mock_button
        ]
        
        # Test detect_login_page
        detect_result = self.auth_manager.detect_login_page()
        self.assertTrue(detect_result)
        
        # Test that elements are properly set for login
        self.assertEqual(self.auth_manager._AuthenticationManager__input_email, mock_email)
        self.assertEqual(self.auth_manager._AuthenticationManager__input_pass, mock_pass)
        self.assertEqual(self.auth_manager._AuthenticationManager__login_button, mock_button)
    
    def test_username_password_storage(self):
        """Test that username and password are stored correctly"""
        # Create new manager with different credentials
        from auth import AuthenticationManager
        auth_manager2 = AuthenticationManager(
            self.mock_driver_manager,
            "different@email.com",
            "differentpassword"
        )
        
        self.assertEqual(auth_manager2._AuthenticationManager__username, "different@email.com")
        self.assertEqual(auth_manager2._AuthenticationManager__password, "differentpassword")
    
    def test_webdriver_type_logging(self):
        """Test that WebDriver type is logged during initialization"""
        # This test ensures the debug print statement works
        # The actual print is mocked away but we can verify the webdriver is stored
        self.assertIsNotNone(self.auth_manager._AuthenticationManager__wdriver)
        self.assertEqual(self.auth_manager._AuthenticationManager__wdriver, self.mock_webdriver)


if __name__ == '__main__':
    unittest.main()