"""
Environment configuration management for Facebook automation.
Handles loading configuration from environment variables and .env files.
"""
import os
from dotenv import load_dotenv
from typing import Optional


class EnvironmentConfig:
    """Manages environment-based configuration for the application."""
    
    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration from environment file.
        
        :param env_file: Path to the environment file (default: .env)
        """
        # Load environment variables from .env file if it exists
        if os.path.exists(env_file):
            load_dotenv(env_file)
    
    @property
    def fb_username(self) -> str:
        """Get Facebook username from environment variables."""
        username = os.getenv("FB_USERNAME")
        if not username:
            raise ValueError("FB_USERNAME not found in environment variables. Please check your .env file.")
        return username
    
    @property
    def fb_password(self) -> str:
        """Get Facebook password from environment variables."""
        password = os.getenv("FB_PASSWORD")
        if not password:
            raise ValueError("FB_PASSWORD not found in environment variables. Please check your .env file.")
        return password
    
    @property
    def fb_login_url(self) -> str:
        """Get Facebook login URL with default fallback."""
        return os.getenv("FB_LOGIN_URL", "https://www.facebook.com/login/")
    
    @property
    def chrome_user_data_dir(self) -> Optional[str]:
        """Get Chrome user data directory path."""
        return os.getenv("CHROME_USER_DATA_DIR")
    
    @property
    def chrome_profile_dir(self) -> str:
        """Get Chrome profile directory with default fallback."""
        return os.getenv("CHROME_PROFILE_DIR", "Default")
    
    @property
    def debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("DEBUG_MODE", "false").lower() in ("true", "1", "yes", "on")
    
    @property
    def headless_mode(self) -> bool:
        """Check if headless mode is enabled."""
        return os.getenv("HEADLESS_MODE", "false").lower() in ("true", "1", "yes", "on")
    
    def validate_config(self) -> bool:
        """
        Validate that all required configuration is present.
        
        :return: True if configuration is valid, False otherwise
        """
        try:
            # Check required fields
            self.fb_username
            self.fb_password
            return True
        except ValueError as e:
            print(f"Configuration validation failed: {e}")
            return False
    
    def print_config_summary(self) -> None:
        """Print a summary of current configuration (without sensitive data)."""
        print("=== Configuration Summary ===")
        print(f"Facebook Login URL: {self.fb_login_url}")
        print(f"Chrome User Data Dir: {self.chrome_user_data_dir or 'Not specified'}")
        print(f"Chrome Profile Dir: {self.chrome_profile_dir}")
        print(f"Debug Mode: {self.debug_mode}")
        print(f"Headless Mode: {self.headless_mode}")
        print(f"Username configured: {'Yes' if os.getenv('FB_USERNAME') else 'No'}")
        print(f"Password configured: {'Yes' if os.getenv('FB_PASSWORD') else 'No'}")
        print("=============================")


# Global instance for easy access
env_config = EnvironmentConfig()