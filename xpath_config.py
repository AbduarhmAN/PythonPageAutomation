"""
XPath selectors configuration for Facebook automation.
Centralizes all XPath selectors with fallback options and maintainability features.
"""
import logging
from typing import List, Dict, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)


class XPathSelectors:
    """
    Centralized XPath selector configuration with fallback options.
    Makes selectors more maintainable when Facebook UI changes.
    """
    
    # Login page selectors (multiple fallbacks)
    LOGIN_EMAIL_SELECTORS = [
        "//input[@name='email']",
        "//input[@type='email']",
        "//input[@id='email']",
        "//input[@placeholder*='email' or @placeholder*='Email']"
    ]
    
    LOGIN_PASSWORD_SELECTORS = [
        "//input[@name='pass']",
        "//input[@name='password']",
        "//input[@type='password']",
        "//input[@id='pass']"
    ]
    
    LOGIN_BUTTON_SELECTORS = [
        "//button[@name='login']",
        "//button[@type='submit']",
        "//input[@type='submit']",
        "//button[contains(text(), 'Log in') or contains(text(), 'Log In')]",
        "//input[@value='Log In']"
    ]
    
    # Account and profile selectors
    ACCOUNT_NAME_SELECTORS = [
        "//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']",
        "//span[contains(@class, 'x1lliihq') and contains(@class, 'x6ikm8r')]",
        "//div[@role='button']//span[text()]",
        "//div[contains(@aria-label, 'Your profile')]//span"
    ]
    
    ACCOUNT_ICON_SELECTORS = [
        "//*[local-name()='g' and @mask='url(#«R1ldm6l6ismipapd5aq»)']",
        "//div[@role='button' and @aria-label]//svg",
        "//div[contains(@class, 'profile')]//img",
        "//a[contains(@href, 'profile')]"
    ]
    
    ALL_PROFILES_BUTTON_SELECTORS = [
        "//*[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f x1dem4cn')]//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft']",
        "//span[contains(text(), 'See all profiles') or contains(text(), 'All profiles')]",
        "//div[@role='menuitem']//span[contains(text(), 'profiles')]",
        "//a[contains(@href, 'profiles') or contains(@href, 'switch')]"
    ]
    
    # Pages container selectors
    PAGES_CONTAINER_SELECTORS = [
        "//div[contains(@class,'x78zum5 xdt5ytf')]//div[contains(@class,'xwxc41k x1y1aw1k')]/div[@class='html-div x11i5rnm x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1oo3vh0 x1rdy4ex' and @role='list']",
        "//div[@role='list']//div[contains(@class, 'x78zum5')]",
        "//div[contains(@class, 'pages')]//div[@role='list']",
        "//ul[contains(@class, 'list')]//li"
    ]
    
    PAGES_FILTER_SELECTORS = [
        "//div[@role='listitem']//*[contains(@class,'x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli xz9dl7a xsag5q8 x4uap5 xkhd6sd x1n2onr6 x1ja2u2z')]//div[@class='x78zum5 xdt5ytf xz62fqu x16ldp7u']/div[@class='xu06os2 x1ok221b']/span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h']",
        "//div[@role='listitem']//span[contains(@class, 'x193iq5w')]",
        "//li//span[text()]",
        "//div[contains(@class, 'page')]//span[text()]"
    ]
    
    CREATE_PAGE_BUTTON_SELECTORS = [
        "//*[contains(@class,'x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli xz9dl7a xsag5q8 x4uap5 xkhd6sd x1n2onr6 x1ja2u2z')]//div[contains(@class,'x78zum5 xdt5ytf xz62fqu x16ldp7u')]//div[contains(@class,'xu06os2 x1ok221b')]//span[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')]",
        "//button[contains(text(), 'Create') and contains(text(), 'Page')]",
        "//a[contains(text(), 'Create') and contains(text(), 'Page')]",
        "//div[@role='button'][contains(text(), 'Create')]"
    ]


class SelectorManager:
    """
    Manages XPath selectors with fallback mechanisms and validation.
    """
    
    def __init__(self, webdriver: WebDriver):
        """
        Initialize SelectorManager with WebDriver instance.
        
        :param webdriver: Selenium WebDriver instance
        """
        self.webdriver = webdriver
        self.selectors = XPathSelectors()
    
    def find_element_with_fallbacks(self, selector_list: List[str], 
                                   timeout: int = 10) -> Optional[WebElement]:
        """
        Try to find element using multiple selector fallbacks.
        
        :param selector_list: List of XPath selectors to try
        :param timeout: Maximum time to wait for element
        :return: WebElement if found, None otherwise
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(self.webdriver, timeout)
        
        for i, selector in enumerate(selector_list):
            try:
                logger.debug(f"Trying selector {i+1}/{len(selector_list)}: {selector}")
                element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                logger.info(f"Element found using selector {i+1}: {selector}")
                return element
            except Exception as e:
                logger.debug(f"Selector {i+1} failed: {e}")
                continue
        
        logger.error(f"All {len(selector_list)} selectors failed to find element")
        return None
    
    def find_elements_with_fallbacks(self, selector_list: List[str]) -> List[WebElement]:
        """
        Try to find elements using multiple selector fallbacks.
        
        :param selector_list: List of XPath selectors to try
        :return: List of WebElements found
        """
        for i, selector in enumerate(selector_list):
            try:
                logger.debug(f"Trying selector {i+1}/{len(selector_list)}: {selector}")
                elements = self.webdriver.find_elements(By.XPATH, selector)
                if elements:
                    logger.info(f"Found {len(elements)} elements using selector {i+1}")
                    return elements
            except Exception as e:
                logger.debug(f"Selector {i+1} failed: {e}")
                continue
        
        logger.error(f"All {len(selector_list)} selectors failed to find elements")
        return []
    
    def get_login_email_element(self) -> Optional[WebElement]:
        """Get login email input element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.LOGIN_EMAIL_SELECTORS)
    
    def get_login_password_element(self) -> Optional[WebElement]:
        """Get login password input element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.LOGIN_PASSWORD_SELECTORS)
    
    def get_login_button_element(self) -> Optional[WebElement]:
        """Get login button element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.LOGIN_BUTTON_SELECTORS)
    
    def get_account_name_element(self) -> Optional[WebElement]:
        """Get account name element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.ACCOUNT_NAME_SELECTORS)
    
    def get_account_icon_element(self) -> Optional[WebElement]:
        """Get account icon element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.ACCOUNT_ICON_SELECTORS)
    
    def get_all_profiles_button_element(self) -> Optional[WebElement]:
        """Get all profiles button element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.ALL_PROFILES_BUTTON_SELECTORS)
    
    def get_pages_container_element(self) -> Optional[WebElement]:
        """Get pages container element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.PAGES_CONTAINER_SELECTORS)
    
    def get_pages_filter_elements(self) -> List[WebElement]:
        """Get pages filter elements with fallbacks."""
        return self.find_elements_with_fallbacks(self.selectors.PAGES_FILTER_SELECTORS)
    
    def get_create_page_button_element(self) -> Optional[WebElement]:
        """Get create page button element with fallbacks."""
        return self.find_element_with_fallbacks(self.selectors.CREATE_PAGE_BUTTON_SELECTORS)
    
    def validate_selector(self, selector: str) -> bool:
        """
        Validate XPath selector syntax.
        
        :param selector: XPath selector to validate
        :return: True if selector syntax is valid
        """
        from validation import InputValidator
        return InputValidator.validate_xpath(selector)
    
    def test_all_selectors(self) -> Dict[str, bool]:
        """
        Test all selectors on current page and return results.
        
        :return: Dictionary mapping selector names to success status
        """
        results = {}
        
        selector_tests = {
            'login_email': self.selectors.LOGIN_EMAIL_SELECTORS,
            'login_password': self.selectors.LOGIN_PASSWORD_SELECTORS,
            'login_button': self.selectors.LOGIN_BUTTON_SELECTORS,
            'account_name': self.selectors.ACCOUNT_NAME_SELECTORS,
            'account_icon': self.selectors.ACCOUNT_ICON_SELECTORS,
            'all_profiles_button': self.selectors.ALL_PROFILES_BUTTON_SELECTORS,
            'pages_container': self.selectors.PAGES_CONTAINER_SELECTORS,
            'pages_filter': self.selectors.PAGES_FILTER_SELECTORS,
            'create_page_button': self.selectors.CREATE_PAGE_BUTTON_SELECTORS
        }
        
        for name, selectors in selector_tests.items():
            try:
                element = self.find_element_with_fallbacks(selectors, timeout=5)
                results[name] = element is not None
            except Exception as e:
                logger.error(f"Error testing {name} selectors: {e}")
                results[name] = False
        
        success_count = sum(results.values())
        total_count = len(results)
        logger.info(f"Selector test completed: {success_count}/{total_count} successful")
        
        return results