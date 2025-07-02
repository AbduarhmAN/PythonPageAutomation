# Configuration Guide

This guide explains how to configure the Python Facebook Page Automation tool for your specific environment and requirements.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Chrome Profile Configuration](#chrome-profile-configuration)
- [Credential Management](#credential-management)
- [XPath Selector Configuration](#xpath-selector-configuration)
- [Environment-Specific Settings](#environment-specific-settings)
- [Security Configuration](#security-configuration)
- [Troubleshooting Configuration](#troubleshooting-configuration)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows (current implementation)
  - macOS and Linux support planned for future releases
- **Python**: Version 3.7 or higher
- **Google Chrome**: Latest stable version recommended
- **Internet Connection**: Required for Facebook access

### Required Python Packages

Install dependencies using pip:
```bash
pip install selenium pyautogui
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

---

## Chrome Profile Configuration

The automation uses an existing Chrome profile to maintain login sessions and avoid repeated authentication.

### Finding Your Chrome Profile

#### Windows
1. Open Chrome and go to `chrome://settings/`
2. Click "You and Google" → "Manage your Google Account"
3. Note your profile name in the top-right corner
4. The profile directory is typically located at:
   ```
   C:\Users\[USERNAME]\AppData\Local\Google\Chrome\User Data\
   ```

#### Profile Directory Structure
```
User Data/
├── Default/          # Profile 0
├── Profile 1/        # Profile 1
├── Profile 2/        # Profile 2
└── ...
```

### Configuring Chrome Profile in Code

Edit `integration.py` in the `Initialze_webdriver()` method:

```python
def Initialze_webdriver(self):
    chrome_options = Options()
    
    # Anti-detection options (recommended to keep)
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # CONFIGURE THESE PATHS FOR YOUR SYSTEM
    chrome_options.add_argument(
        "user-data-dir=C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data"
    )
    chrome_options.add_argument("profile-directory=Profile X")  # Replace X with your profile number
    
    self.__wdriver = webdriver.Chrome(options=chrome_options)
    self.__wdriver.maximize_window()
```

### Profile Selection Tips

1. **Use a Dedicated Profile**: Create a new Chrome profile specifically for automation
2. **Login to Facebook First**: Manually login to Facebook in the selected profile
3. **Save Login Information**: Allow Chrome to save your Facebook login for seamless automation
4. **Test Profile Access**: Verify the profile path is correct before running automation

### Creating a New Chrome Profile

1. Open Chrome
2. Click the profile icon in the top-right corner
3. Select "Add" → "Create new profile"
4. Name it "Automation" or similar
5. Note the profile directory name (usually "Profile X")

---

## Credential Management

### Current Implementation (Insecure)

⚠️ **Security Warning**: The current implementation hardcodes credentials in `fb_atumation.py`:

```python
def __init__(self):
    # ⚠️ INSECURE - Replace with secure method
    self.username = "maghrbi006@hotmail.com"
    self.password = "Maghrbi##007"
```

### Recommended Secure Configurations

#### Option 1: Environment Variables

1. Create a `.env` file (add to `.gitignore`):
```bash
FB_USERNAME=your_email@example.com
FB_PASSWORD=your_secure_password
```

2. Update `fb_atumation.py`:
```python
import os
from dotenv import load_dotenv

class ApplicationController:
    def __init__(self):
        load_dotenv()  # Load .env file
        
        self.username = os.getenv('FB_USERNAME')
        self.password = os.getenv('FB_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("Username and password must be set in environment variables")
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

#### Option 2: Configuration File

1. Create `config.json` (add to `.gitignore`):
```json
{
    "facebook": {
        "username": "your_email@example.com",
        "password": "your_secure_password"
    },
    "chrome": {
        "profile_path": "C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data",
        "profile_directory": "Profile 4"
    }
}
```

2. Update `fb_atumation.py`:
```python
import json

class ApplicationController:
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        self.username = config['facebook']['username']
        self.password = config['facebook']['password']
```

#### Option 3: Command Line Arguments

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='Facebook Page Automation')
    parser.add_argument('--username', required=True, help='Facebook username')
    parser.add_argument('--password', required=True, help='Facebook password')
    
    args = parser.parse_args()
    
    app = ApplicationController(args.username, args.password)
    app.run()

if __name__ == "__main__":
    main()
```

Usage:
```bash
python fb_atumation.py --username your_email@example.com --password your_password
```

---

## XPath Selector Configuration

Facebook frequently updates their UI, which may break XPath selectors. The selectors are stored in `config.py` within the `DataManager` class.

### Current Selectors

```python
class DataManager:
    # Account identification
    account_name = "//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']"
    
    # Navigation elements
    account_icon = "//*[local-name()='g' and @mask='url(#«R1ldm6l6ismipapd5aq»)']"
    all_profiles_button = "//*[contains(@class,'x193iq5w xeuugli x13faqbe...')]"
    
    # Page management
    pages_containter = "//div[contains(@class,'x78zum5 xdt5ytf')]//div[...]"
    pages_filter = "//div[@role='listitem']//*[contains(@class,'x1qjc9v5...')]"
```

### Updating Selectors

When Facebook updates their interface:

1. **Use Browser Developer Tools**:
   - Right-click on the element
   - Select "Inspect" or "Inspect Element"
   - Right-click on the HTML element
   - Choose "Copy" → "Copy XPath"

2. **Test Selectors**:
   ```python
   # Test in browser console
   $x("YOUR_XPATH_HERE")
   ```

3. **Update `config.py`**:
   ```python
   # Replace the broken selector
   account_name = "NEW_XPATH_SELECTOR"
   ```

### Selector Best Practices

- **Use Stable Attributes**: Prefer `id`, `name`, or `data-*` attributes over CSS classes
- **Avoid Generated Classes**: Facebook uses auto-generated CSS classes that change frequently
- **Use Partial Matches**: Use `contains()` for more resilient selectors
- **Test Thoroughly**: Verify selectors work across different account types

### Fallback Selectors

Consider implementing fallback selectors:

```python
class DataManager:
    # Primary selector
    account_name = "//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']"
    
    # Fallback selectors
    account_name_fallback = [
        "//span[contains(@class, 'account-name')]",
        "//div[@data-testid='account-name']//span",
        "//*[contains(text(), '@')]"  # Email-like text
    ]
```

---

## Environment-Specific Settings

### Development vs Production

#### Development Configuration
```python
class Config:
    DEBUG = True
    HEADLESS = False  # Show browser for debugging
    IMPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    SCREENSHOT_ON_ERROR = True
```

#### Production Configuration
```python
class Config:
    DEBUG = False
    HEADLESS = True   # Run without UI
    IMPLICIT_WAIT = 5
    PAGE_LOAD_TIMEOUT = 15
    SCREENSHOT_ON_ERROR = False
```

### Cross-Platform Chrome Paths

```python
import platform
import os

def get_chrome_user_data_dir():
    system = platform.system()
    
    if system == "Windows":
        return os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif system == "Linux":
        return os.path.expanduser("~/.config/google-chrome")
    else:
        raise OSError(f"Unsupported operating system: {system}")
```

### Logging Configuration

Create a `logging_config.py`:

```python
import logging
import os
from datetime import datetime

def setup_logging(debug=False):
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging level
    level = logging.DEBUG if debug else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(
        f'logs/automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

---

## Security Configuration

### Chrome Security Options

```python
def setup_secure_chrome_options():
    chrome_options = Options()
    
    # Basic security
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    # Privacy options
    chrome_options.add_argument("--incognito")  # Use with caution - may break login persistence
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Anti-detection (current implementation)
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    return chrome_options
```

### Network Security

```python
import requests
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings (use with caution)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Use proxy if required
PROXY_CONFIG = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}
```

### Rate Limiting Configuration

```python
import time
import random

class RateLimiter:
    def __init__(self, min_delay=1, max_delay=3):
        self.min_delay = min_delay
        self.max_delay = max_delay
    
    def wait(self):
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

# Usage
rate_limiter = RateLimiter(min_delay=2, max_delay=5)
rate_limiter.wait()  # Random delay between actions
```

---

## Troubleshooting Configuration

### Common Configuration Issues

#### 1. Chrome Profile Path Errors

**Error**: `selenium.common.exceptions.InvalidArgumentException: Message: invalid argument: user data directory is already in use`

**Solution**:
```python
# Ensure Chrome is fully closed before running automation
chrome_options.add_argument("--remote-debugging-port=9222")
```

#### 2. Element Not Found Errors

**Error**: `selenium.common.exceptions.NoSuchElementException`

**Solution**:
```python
# Add implicit waits
driver.implicitly_wait(10)

# Use explicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
```

#### 3. Login Failures

**Error**: Login automation fails or gets stuck

**Solutions**:
- Verify credentials are correct
- Check for 2FA requirements
- Ensure Chrome profile has valid session
- Handle CAPTCHA challenges manually

### Debug Configuration

Enable detailed debugging:

```python
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

# Enable Selenium logging
LOGGER.setLevel(logging.DEBUG)

# Enable Chrome driver logging
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--v=1")
```

### Performance Configuration

```python
# Optimize for speed
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")  # Use with caution
chrome_options.add_argument("--disable-css")
chrome_options.add_argument("--disable-plugins")

# Set timeouts
driver.set_page_load_timeout(30)
driver.implicitly_wait(10)
```

---

## Configuration File Template

Create a comprehensive `config.yaml`:

```yaml
# Facebook Automation Configuration

facebook:
  login_url: "https://www.facebook.com/login/"
  base_url: "https://www.facebook.com"

chrome:
  profile_path: "C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data"
  profile_directory: "Profile 4"
  headless: false
  maximize_window: true
  
timeouts:
  page_load: 30
  implicit_wait: 10
  explicit_wait: 15
  
delays:
  min_action_delay: 1
  max_action_delay: 3
  login_delay: 10
  
logging:
  level: "INFO"
  file_enabled: true
  console_enabled: true
  
security:
  anti_detection: true
  stealth_mode: true
  
selectors:
  account_name: "//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']"
  account_icon: "//*[local-name()='g' and @mask='url(#«R1ldm6l6ismipapd5aq»)']"
  # Add other selectors here
```

Load with:
```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
```

---

## Next Steps

After configuring the tool:

1. **Test Basic Functionality**: Run a simple login test
2. **Verify Profile Access**: Ensure the Chrome profile works correctly
3. **Test Element Detection**: Verify XPath selectors are working
4. **Monitor Performance**: Check for rate limiting or detection issues
5. **Implement Security**: Add proper credential management
6. **Add Logging**: Implement comprehensive logging for debugging

For additional help, refer to the [API Reference](API_REFERENCE.md) and [README](README.md).