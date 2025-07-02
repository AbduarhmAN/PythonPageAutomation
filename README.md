# Python Facebook Page Automation

A comprehensive Python automation tool for managing Facebook pages and profiles using Selenium WebDriver and PyAutoGUI.

## Overview

This project provides an automated solution for:
- Facebook authentication and login
- Account and page management
- Profile navigation and interaction
- Page content automation

The tool uses a combination of Selenium WebDriver for web automation and PyAutoGUI for enhanced interaction simulation, making the automation more human-like and harder to detect.

## Features

- **Automated Facebook Login**: Secure authentication with customizable credentials
- **Profile Management**: Navigate between different Facebook profiles and pages
- **Page Discovery**: Automatically retrieve and filter account pages
- **Modular Architecture**: Clean separation of concerns with dedicated managers
- **Chrome Profile Integration**: Uses existing Chrome profiles for seamless operation
- **Human-like Interactions**: Combines Selenium with PyAutoGUI for natural mouse movements

## Project Structure

```
PythonPageAutomation/
├── fb_atumation.py      # Main application controller
├── auth.py              # Authentication management
├── integration.py       # Selenium WebDriver and PyAutoGUI integration
├── config.py           # Configuration and data management
├── upload.py           # Content upload functionality (placeholder)
├── post_automation.py  # Post automation features (placeholder)
├── retrieval.py        # Content retrieval features (placeholder)
├── cleanup.py          # Cleanup and maintenance (placeholder)
└── README.md           # This documentation
```

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Chrome WebDriver (automatically managed by Selenium)
- Windows environment (for current Chrome profile paths)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AbduarhmAN/PythonPageAutomation.git
cd PythonPageAutomation
```

2. Install required dependencies:
```bash
pip install selenium pyautogui
```

3. Configure your credentials and Chrome profile path in `fb_atumation.py`

4. Run the automation:
```bash
python fb_atumation.py
```

## Configuration

### Chrome Profile Setup

The automation uses an existing Chrome profile to maintain session state and avoid repeated logins. Update the Chrome profile path in `integration.py`:

```python
chrome_options.add_argument("user-data-dir=C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("profile-directory=Profile X")
```

### Credentials Configuration

**⚠️ Security Warning**: Never commit credentials to version control. Consider using environment variables or a secure configuration file.

Update credentials in `fb_atumation.py`:
```python
self.username = "your_email@example.com"
self.password = "your_secure_password"
```

## Architecture

### Core Components

#### ApplicationController (`fb_atumation.py`)
The main orchestrator that coordinates all automation activities:
- Initializes all manager components
- Executes the complete automation workflow
- Handles error management and logging

#### AuthenticationManager (`auth.py`)
Manages Facebook login and authentication:
- Opens Facebook login page
- Detects login form elements
- Performs automated login with credentials
- Handles login form interactions

#### SeleniumManager (`integration.py`)
Handles WebDriver management and enhanced interactions:
- Initializes Chrome WebDriver with stealth options
- Provides enhanced element interaction methods
- Combines Selenium with PyAutoGUI for natural movements

#### ConfigManager & DataManager (`config.py`)
Manages configuration and data processing:
- Stores XPath selectors for Facebook elements
- Filters and processes page information
- Handles account and page data management

## Usage Examples

### Basic Automation Run
```python
from fb_atumation import ApplicationController

# Initialize and run automation
app = ApplicationController()
app.run()
```

### Custom Authentication
```python
from auth import AuthenticationManager
from integration import SeleniumManager

# Initialize components
driver_manager = SeleniumManager()
driver_manager.Initialze_webdriver()

auth_manager = AuthenticationManager(
    driver_manager, 
    "your_email@example.com", 
    "your_password"
)

# Perform login
auth_manager.open_login_page()
if auth_manager.detect_login_page():
    auth_manager.preform_login()
```

### Page Management
```python
from config import ConfigManager

# Initialize configuration manager
config_manager = ConfigManager(main_page="Your Main Page Name")

# Retrieve and filter account pages
pages = config_manager.getAccountPages()
print(f"Found {len(pages)} pages")
```

## API Reference

### ApplicationController

#### Methods:
- `__init__()`: Initializes all components and managers
- `login()`: Executes the login sequence
- `setup_account_ui()`: Navigates to account pages interface
- `retrieve_account_pages()`: Retrieves and processes account pages
- `run()`: Executes the complete automation workflow

### AuthenticationManager

#### Methods:
- `__init__(driverManager, username, password)`: Initialize with credentials
- `open_login_page()`: Navigate to Facebook login page
- `detect_login_page()`: Check if login elements are present
- `preform_login()`: Execute automated login process

### SeleniumManager

#### Methods:
- `Initialze_webdriver()`: Set up Chrome WebDriver with stealth options
- `get_webdriver()`: Return the WebDriver instance
- `navigate_to_elem(element)`: Move mouse to element naturally
- `clickOnScreen()`: Perform mouse click

### ConfigManager

#### Methods:
- `__init__(main_page, current_account, pages_on_account)`: Initialize configuration
- `getAccountPages()`: Retrieve and filter account pages
- `_filter_pages(pages, account, skip_last)`: Apply filtering logic to pages

## Security Considerations

### Credential Management
- **Never hardcode credentials** in source code
- Use environment variables or secure configuration files
- Consider using OAuth or app-specific passwords where available

### Chrome Profile Security
- Ensure Chrome profile contains only necessary login sessions
- Use dedicated Chrome profiles for automation
- Regularly review and clean browser data

### Rate Limiting
- Implement delays between actions to avoid detection
- Use random intervals for more natural behavior
- Monitor for CAPTCHA or security challenges

## Troubleshooting

### Common Issues

#### Chrome Profile Path Errors
```
Solution: Verify the Chrome profile path exists and is accessible
- Check Windows username in path
- Ensure Chrome profile directory exists
- Verify profile number is correct
```

#### Element Not Found Errors
```
Solution: Facebook UI changes frequently
- Update XPath selectors in config.py
- Check if Facebook has updated their interface
- Enable debug logging to see element states
```

#### Login Failures
```
Solution: Multiple potential causes
- Verify credentials are correct
- Check for CAPTCHA or 2FA requirements
- Ensure Chrome profile has required permissions
- Clear browser cache and cookies
```

### Debug Mode

Enable debug output by adding logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Test thoroughly
6. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all classes and methods
- Include type hints where appropriate
- Add error handling for external dependencies

### Testing
- Test with multiple Facebook accounts
- Verify compatibility with different Chrome versions
- Test on different Windows configurations

## Roadmap

### Planned Features
- [ ] Content upload automation (`upload.py`)
- [ ] Post scheduling and management (`post_automation.py`)
- [ ] Advanced content retrieval (`retrieval.py`)
- [ ] Automated cleanup and maintenance (`cleanup.py`)
- [ ] Cross-platform support (macOS, Linux)
- [ ] Configuration file support
- [ ] Enhanced error handling and recovery
- [ ] Headless browser support

## License

This project is provided for educational purposes. Please ensure compliance with Facebook's Terms of Service and applicable laws when using this automation tool.

## Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with Facebook's Terms of Service and all applicable laws. The authors are not responsible for any misuse or violations that may occur.

## Documentation

For detailed information, please refer to the complete documentation:

- **[API Reference](API_REFERENCE.md)** - Complete API documentation for all classes and methods
- **[Configuration Guide](CONFIGURATION.md)** - Detailed setup and configuration instructions
- **[Security Guide](SECURITY.md)** - Security best practices and credential management
- **[Contributing Guidelines](CONTRIBUTING.md)** - Development standards and contribution process
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Common issues and debugging techniques

## Support

For issues, questions, or contributions, please use the GitHub issue tracker or submit pull requests.