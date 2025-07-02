# Facebook Page Automation Tool

A Python-based automation tool for managing Facebook pages and accounts using Selenium WebDriver.

## ⚠️ Important Notice

This tool is for educational and legitimate business purposes only. Please ensure you:
- Have proper authorization to automate Facebook accounts
- Comply with Facebook's Terms of Service
- Use this tool responsibly and ethically
- Respect rate limits and avoid spamming

## Features

- Automated Facebook login with credential management
- Account page retrieval and filtering
- Extensible architecture for additional automation tasks
- Cross-platform browser support
- Environment-based configuration

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Valid Facebook account credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AbduarhmAN/PythonPageAutomation.git
cd PythonPageAutomation
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your credentials and configuration
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required: Facebook Login Credentials
FB_USERNAME=your_email@example.com
FB_PASSWORD=your_password_here

# Optional: Chrome Configuration
CHROME_USER_DATA_DIR=/path/to/chrome/user/data
CHROME_PROFILE_DIR=Default

# Optional: Application Settings
FB_LOGIN_URL=https://www.facebook.com/login/
DEBUG_MODE=false
HEADLESS_MODE=false
```

### Chrome Profile Setup

For best results, configure a dedicated Chrome profile:
1. Open Chrome and create a new profile
2. Log into Facebook manually in this profile
3. Note the profile directory path
4. Update the `.env` file with the correct paths

## Usage

### Basic Usage

```python
from fb_automation import ApplicationController

# Initialize and run the automation
app = ApplicationController()
app.run()
```

### Advanced Usage

```python
from auth import AuthenticationManager
from integration import SeleniumManager
from config import ConfigManager

# Initialize components separately for more control
driver_manager = SeleniumManager()
driver_manager.initialize_webdriver()

auth_manager = AuthenticationManager(
    driver_manager, 
    "username", 
    "password"
)

# Perform login
if auth_manager.open_login_page():
    if auth_manager.detect_login_page():
        auth_manager.perform_login()
```

## Project Structure

```
PythonPageAutomation/
│
├── fb_automation.py      # Main application controller
├── auth.py              # Authentication management
├── integration.py       # Selenium WebDriver integration
├── config.py           # Configuration and data management
├── post_automation.py  # Post automation features (future)
├── upload.py           # Content upload features (future)
├── cleanup.py          # Cleanup utilities (future)
├── retrieval.py        # Data retrieval features (future)
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all classes and methods
- Handle exceptions appropriately

### Testing

Currently, this project doesn't have automated tests. Contributions for test coverage are welcome.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Chrome not found**: Ensure Chrome is installed and accessible
2. **Login fails**: Check credentials and Facebook security settings
3. **Elements not found**: Facebook UI changes frequently; XPath selectors may need updates
4. **Permission denied**: Run with appropriate permissions for Chrome profile access

### Debug Mode

Enable debug mode in your `.env` file:
```env
DEBUG_MODE=true
```

This will provide more detailed logging and error information.

## Security Considerations

- Never commit credentials to version control
- Use environment variables for sensitive data
- Consider using dedicated Facebook developer accounts
- Regularly rotate passwords and review access logs
- Be aware of Facebook's automation detection

## Limitations

- Depends on Facebook's UI structure (subject to change)
- Rate limits may apply
- Some features require specific Facebook account permissions
- Browser automation may be detected by Facebook's systems

## License

This project is provided as-is for educational purposes. Users are responsible for ensuring compliance with all applicable terms of service and laws.

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review Facebook's developer documentation
3. Open an issue on GitHub with detailed information

## Disclaimer

This tool is not affiliated with or endorsed by Facebook. Use at your own risk and ensure compliance with Facebook's Terms of Service.