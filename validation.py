"""
Input validation utilities for Facebook automation.
Provides validation functions for various input types and data.
"""
import re
import os
import logging
from typing import Optional, List, Union
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class InputValidator:
    """Provides input validation methods for automation parameters."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        :param email: Email address to validate
        :return: True if email format is valid
        """
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> bool:
        """
        Validate password strength.
        
        :param password: Password to validate
        :param min_length: Minimum required password length
        :return: True if password meets requirements
        """
        if not password or not isinstance(password, str):
            return False
        
        if len(password) < min_length:
            return False
        
        # Check for at least one letter and one number
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        
        return has_letter and has_number
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        :param url: URL to validate
        :return: True if URL format is valid
        """
        if not url or not isinstance(url, str):
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def validate_file_path(file_path: str, check_exists: bool = True) -> bool:
        """
        Validate file path format and existence.
        
        :param file_path: File path to validate
        :param check_exists: Whether to check if file actually exists
        :return: True if file path is valid
        """
        if not file_path or not isinstance(file_path, str):
            return False
        
        # Check path format
        if not os.path.isabs(file_path) and not os.path.isfile(file_path):
            # If not absolute, check if it's a valid relative path
            if not file_path.replace('\\', '/').replace('./', ''):
                return False
        
        if check_exists:
            return os.path.exists(file_path)
        
        return True
    
    @staticmethod
    def validate_chrome_profile_path(user_data_dir: str, profile_dir: str) -> bool:
        """
        Validate Chrome profile paths.
        
        :param user_data_dir: Chrome user data directory path
        :param profile_dir: Chrome profile directory name
        :return: True if paths are valid
        """
        if not user_data_dir or not profile_dir:
            return False
        
        if not os.path.exists(user_data_dir):
            logger.warning(f"Chrome user data directory not found: {user_data_dir}")
            return False
        
        profile_path = os.path.join(user_data_dir, profile_dir)
        if not os.path.exists(profile_path):
            logger.warning(f"Chrome profile directory not found: {profile_path}")
            return False
        
        return True
    
    @staticmethod
    def validate_xpath(xpath: str) -> bool:
        """
        Basic validation of XPath syntax.
        
        :param xpath: XPath expression to validate
        :return: True if XPath syntax appears valid
        """
        if not xpath or not isinstance(xpath, str):
            return False
        
        # Basic checks for common XPath syntax
        if not xpath.strip():
            return False
        
        # Check for balanced brackets
        open_brackets = xpath.count('[')
        close_brackets = xpath.count(']')
        if open_brackets != close_brackets:
            return False
        
        # Check for balanced parentheses
        open_parens = xpath.count('(')
        close_parens = xpath.count(')')
        if open_parens != close_parens:
            return False
        
        return True
    
    @staticmethod
    def sanitize_text_input(text: str, max_length: int = 5000) -> str:
        """
        Sanitize text input for posting.
        
        :param text: Text to sanitize
        :param max_length: Maximum allowed text length
        :return: Sanitized text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Remove or replace potentially problematic characters
        text = text.strip()
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
            logger.warning(f"Text truncated to {max_length} characters")
        
        return text
    
    @staticmethod
    def validate_config_dict(config: dict, required_keys: List[str]) -> bool:
        """
        Validate configuration dictionary has required keys.
        
        :param config: Configuration dictionary to validate
        :param required_keys: List of required key names
        :return: True if all required keys are present
        """
        if not isinstance(config, dict):
            return False
        
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            logger.error(f"Missing required configuration keys: {missing_keys}")
            return False
        
        return True


def validate_automation_inputs(username: str, password: str, 
                             chrome_user_data_dir: Optional[str] = None,
                             chrome_profile_dir: Optional[str] = None) -> bool:
    """
    Validate all automation input parameters.
    
    :param username: Facebook username/email
    :param password: Facebook password
    :param chrome_user_data_dir: Optional Chrome user data directory
    :param chrome_profile_dir: Optional Chrome profile directory
    :return: True if all inputs are valid
    """
    validator = InputValidator()
    
    # Validate email
    if not validator.validate_email(username):
        logger.error(f"Invalid email format: {username}")
        return False
    
    # Validate password
    if not validator.validate_password(password):
        logger.error("Invalid password: must be at least 6 characters with letters and numbers")
        return False
    
    # Validate Chrome paths if provided
    if chrome_user_data_dir and chrome_profile_dir:
        if not validator.validate_chrome_profile_path(chrome_user_data_dir, chrome_profile_dir):
            logger.error("Invalid Chrome profile configuration")
            return False
    
    logger.info("All automation inputs validated successfully")
    return True