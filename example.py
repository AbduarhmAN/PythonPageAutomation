#!/usr/bin/env python3
"""
Example usage script for Facebook Page Automation.
Demonstrates how to use the automation framework safely.
"""
import sys
import os
import logging
from fb_automation import ApplicationController, main
from env_config import env_config

# Configure logging for example
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment():
    """Check if environment is properly configured."""
    logger.info("Checking environment configuration...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        logger.error("No .env file found. Please create one based on .env.example")
        return False
    
    # Validate configuration
    if not env_config.validate_config():
        logger.error("Environment configuration is invalid")
        return False
    
    logger.info("Environment configuration is valid")
    return True


def run_basic_automation():
    """Run basic automation example."""
    logger.info("Starting basic Facebook automation example...")
    
    if not check_environment():
        logger.error("Environment check failed. Please fix configuration before running.")
        return False
    
    try:
        # Run the automation
        success = main()
        
        if success:
            logger.info("Automation completed successfully!")
        else:
            logger.error("Automation failed. Check logs for details.")
        
        return success
        
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


def run_custom_automation():
    """Example of custom automation flow."""
    logger.info("Starting custom automation example...")
    
    if not check_environment():
        return False
    
    try:
        # Create application controller
        app = ApplicationController()
        
        # Custom flow - just login and test selectors
        if app.login():
            logger.info("Login successful! Testing selectors...")
            
            # Test all selectors on current page
            results = app.selector_manager.test_all_selectors()
            
            success_count = sum(results.values())
            total_count = len(results)
            
            logger.info(f"Selector test results: {success_count}/{total_count} successful")
            
            for selector_name, success in results.items():
                status = "✓" if success else "✗"
                logger.info(f"  {status} {selector_name}")
            
            # Cleanup
            app.cleanup_manager.complete_cleanup()
            return True
        else:
            logger.error("Login failed")
            return False
            
    except Exception as e:
        logger.error(f"Custom automation error: {e}")
        return False


def main_example():
    """Main function for examples."""
    if len(sys.argv) > 1 and sys.argv[1] == "--custom":
        return run_custom_automation()
    else:
        return run_basic_automation()


if __name__ == "__main__":
    print("Facebook Page Automation - Example Usage")
    print("=" * 40)
    print()
    print("Usage:")
    print("  python example.py           # Run basic automation")
    print("  python example.py --custom  # Run custom automation example")
    print()
    print("Make sure you have:")
    print("1. Created a .env file with your Facebook credentials")
    print("2. Installed dependencies: pip install -r requirements.txt")
    print("3. Chrome browser installed")
    print()
    
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    success = main_example()
    exit_code = 0 if success else 1
    sys.exit(exit_code)