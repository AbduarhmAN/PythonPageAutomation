"""
Unit tests for config.py - DataManager and ConfigManager classes
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DataManager, ConfigManager


class TestDataManager(unittest.TestCase):
    """Test cases for DataManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data_manager = DataManager()
    
    def test_initialization(self):
        """Test DataManager initialization"""
        self.assertEqual(self.data_manager.mainPage, "")
        self.assertIsInstance(self.data_manager.account_pages, list)
        self.assertEqual(len(self.data_manager.account_pages), 0)
    
    def test_xpath_selectors_exist(self):
        """Test that all required XPath selectors are defined"""
        self.assertIsInstance(self.data_manager.account_name, str)
        self.assertIsInstance(self.data_manager.create_page_button, str)
        self.assertIsInstance(self.data_manager.account_icon, str)
        self.assertIsInstance(self.data_manager.all_profiles_button, str)
        self.assertIsInstance(self.data_manager.pages_containter, str)
        self.assertIsInstance(self.data_manager.pages_filter, str)
        
        # Check that selectors are not empty
        self.assertTrue(len(self.data_manager.account_name) > 0)
        self.assertTrue(len(self.data_manager.create_page_button) > 0)
        self.assertTrue(len(self.data_manager.account_icon) > 0)
        self.assertTrue(len(self.data_manager.all_profiles_button) > 0)
        self.assertTrue(len(self.data_manager.pages_containter) > 0)
        self.assertTrue(len(self.data_manager.pages_filter) > 0)


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_web_element = Mock()
        self.config_manager = ConfigManager(
            main_page="Test Main Page",
            current_account="Test Account",
            pages_on_account=self.mock_web_element
        )
    
    def test_initialization(self):
        """Test ConfigManager initialization"""
        self.assertEqual(self.config_manager.mainPage, "Test Main Page")
        self.assertEqual(self.config_manager.currentAccount, "Test Account")
        self.assertEqual(self.config_manager.PagesOnAccount, self.mock_web_element)
        self.assertIsInstance(self.config_manager.dataMgr, DataManager)
        self.assertEqual(self.config_manager.dataMgr.mainPage, "Test Main Page")
    
    def test_initialization_with_defaults(self):
        """Test ConfigManager initialization with default values"""
        config_manager = ConfigManager()
        self.assertEqual(config_manager.mainPage, "")
        self.assertEqual(config_manager.currentAccount, "")
        self.assertIsNone(config_manager.PagesOnAccount)
        self.assertEqual(config_manager.dataMgr.mainPage, "")
    
    def test_getAccountPages_with_mock_elements(self):
        """Test getAccountPages method with mock elements"""
        # Create mock page elements
        mock_page1 = Mock()
        mock_page1.text = "Page 1"
        mock_page2 = Mock()
        mock_page2.text = "Page 2"
        mock_page3 = Mock()
        mock_page3.text = "Test Account"  # Same as current account, should be filtered
        mock_page4 = Mock()
        mock_page4.text = "Page 4"
        
        mock_pages = [mock_page1, mock_page2, mock_page3, mock_page4]
        
        # Mock the container element's find_elements method
        self.mock_web_element.find_elements.return_value = mock_pages
        
        # Test method
        result = self.config_manager.getAccountPages()
        
        # Verify find_elements was called with correct parameters
        self.mock_web_element.find_elements.assert_called_once_with(
            by="xpath", value=self.config_manager.dataMgr.pages_filter
        )
        
        # Result should exclude the page with same name as current account
        self.assertEqual(len(result), 3)
        self.assertIn(mock_page1, result)
        self.assertIn(mock_page2, result)
        self.assertNotIn(mock_page3, result)  # Filtered out
        self.assertIn(mock_page4, result)
    
    def test_getAccountPages_with_main_page_skip_last(self):
        """Test getAccountPages with main page (should skip last element)"""
        # Set current account to main page
        self.config_manager.currentAccount = "Test Main Page"
        self.config_manager.dataMgr.mainPage = "Test Main Page"
        
        # Create mock page elements
        mock_page1 = Mock()
        mock_page1.text = "Page 1"
        mock_page2 = Mock()
        mock_page2.text = "Page 2"
        mock_page3 = Mock()
        mock_page3.text = "Page 3"  # This should be skipped as last element
        
        mock_pages = [mock_page1, mock_page2, mock_page3]
        self.mock_web_element.find_elements.return_value = mock_pages
        
        result = self.config_manager.getAccountPages()
        
        # Should skip the last element when current account is main page
        self.assertEqual(len(result), 2)
        self.assertIn(mock_page1, result)
        self.assertIn(mock_page2, result)
        self.assertNotIn(mock_page3, result)  # Last element skipped
    
    def test_getAccountPages_with_exception(self):
        """Test getAccountPages method when find_elements raises exception"""
        # Mock find_elements to raise an exception
        self.mock_web_element.find_elements.side_effect = Exception("Element not found")
        
        result = self.config_manager.getAccountPages()
        
        # Should return empty list when exception occurs
        self.assertEqual(result, [])
    
    def test_getAccountPages_with_custom_parameters(self):
        """Test getAccountPages with custom parameters"""
        custom_element = Mock()
        mock_page = Mock()
        mock_page.text = "Custom Page"
        custom_element.find_elements.return_value = [mock_page]
        
        result = self.config_manager.getAccountPages(
            cAccount="Custom Account",
            unorgnizedElements=custom_element
        )
        
        custom_element.find_elements.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Custom Page")
    
    def test_filter_pages_basic_filtering(self):
        """Test _filter_pages method with basic filtering"""
        # Create mock pages
        mock_page1 = Mock()
        mock_page1.text = "Page 1"
        mock_page2 = Mock()
        mock_page2.text = ""  # Empty text, should be filtered
        mock_page3 = Mock()
        mock_page3.text = "Test Account"  # Same as account, should be filtered
        mock_page4 = Mock()
        mock_page4.text = "   "  # Whitespace only, should be filtered
        mock_page5 = Mock()
        mock_page5.text = "Page 5"
        
        pages = [mock_page1, mock_page2, mock_page3, mock_page4, mock_page5]
        
        result = self.config_manager._filter_pages(pages, "Test Account", False)
        
        # Should only include pages with non-empty text different from account name
        self.assertEqual(len(result), 2)
        self.assertIn(mock_page1, result)
        self.assertIn(mock_page5, result)
    
    def test_filter_pages_skip_last(self):
        """Test _filter_pages method with skip_last=True"""
        mock_page1 = Mock()
        mock_page1.text = "Page 1"
        mock_page2 = Mock()
        mock_page2.text = "Page 2"
        mock_page3 = Mock()
        mock_page3.text = "Last Page"
        
        pages = [mock_page1, mock_page2, mock_page3]
        
        result = self.config_manager._filter_pages(pages, "Test Account", True)
        
        # Should skip the last element
        self.assertEqual(len(result), 2)
        self.assertIn(mock_page1, result)
        self.assertIn(mock_page2, result)
        self.assertNotIn(mock_page3, result)
    
    def test_filter_pages_with_exception(self):
        """Test _filter_pages method when page.text raises exception"""
        mock_page1 = Mock()
        mock_page1.text = "Page 1"
        mock_page2 = Mock()
        mock_page2.text.side_effect = Exception("Text access failed")
        mock_page3 = Mock()
        mock_page3.text = "Page 3"
        
        pages = [mock_page1, mock_page2, mock_page3]
        
        result = self.config_manager._filter_pages(pages, "Test Account", False)
        
        # Should handle exception gracefully and continue
        self.assertEqual(len(result), 2)
        self.assertIn(mock_page1, result)
        self.assertIn(mock_page3, result)
        self.assertNotIn(mock_page2, result)


if __name__ == '__main__':
    unittest.main()