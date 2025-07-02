# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Python Facebook Page Automation tool.

## Table of Contents

- [Common Issues](#common-issues)
- [Installation Problems](#installation-problems)
- [Configuration Issues](#configuration-issues)
- [Runtime Errors](#runtime-errors)
- [Performance Issues](#performance-issues)
- [Security & Detection Issues](#security--detection-issues)
- [Debugging Tools](#debugging-tools)
- [Getting Support](#getting-support)

---

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'selenium'"

**Symptoms:**
```
Traceback (most recent call last):
  File "fb_atumation.py", line 3, in <module>
    from integration import SeleniumManager
  File "integration.py", line 1, in <module>
    from selenium import webdriver
ModuleNotFoundError: No module named 'selenium'
```

**Solutions:**
1. **Install Selenium:**
   ```bash
   pip install selenium
   ```

2. **Install all requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check virtual environment:**
   ```bash
   # Activate virtual environment first
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install selenium
   ```

**Verification:**
```bash
python -c "import selenium; print(selenium.__version__)"
```

---

### Issue: Chrome Profile Path Errors

**Symptoms:**
```
selenium.common.exceptions.InvalidArgumentException: Message: invalid argument: user data directory is already in use
```

**Solutions:**

1. **Close all Chrome instances:**
   ```bash
   # Windows
   taskkill /f /im chrome.exe
   
   # macOS
   killall "Google Chrome"
   
   # Linux
   pkill chrome
   ```

2. **Use different profile:**
   ```python
   # In integration.py, change profile directory
   chrome_options.add_argument("profile-directory=Profile 5")  # Try different number
   ```

3. **Create dedicated automation profile:**
   ```python
   import tempfile
   temp_profile = tempfile.mkdtemp()
   chrome_options.add_argument(f"user-data-dir={temp_profile}")
   ```

4. **Fix profile path:**
   ```python
   # Windows
   chrome_options.add_argument("user-data-dir=C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data")
   
   # macOS
   chrome_options.add_argument("user-data-dir=/Users/YOUR_USERNAME/Library/Application Support/Google/Chrome")
   
   # Linux
   chrome_options.add_argument("user-data-dir=/home/YOUR_USERNAME/.config/google-chrome")
   ```

---

### Issue: Element Not Found Errors

**Symptoms:**
```
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element
```

**Causes:**
- Facebook UI has changed
- Page hasn't loaded completely
- Element is hidden or not visible
- XPath selector is incorrect

**Solutions:**

1. **Add explicit waits:**
   ```python
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   from selenium.webdriver.common.by import By
   
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
   ```

2. **Update XPath selectors:**
   ```python
   # Check current Facebook UI and update in config.py
   # Use browser dev tools to find new selectors
   ```

3. **Add retry logic:**
   ```python
   def find_element_with_retry(driver, xpath, max_attempts=3):
       for attempt in range(max_attempts):
           try:
               return driver.find_element(By.XPATH, xpath)
           except NoSuchElementException:
               if attempt == max_attempts - 1:
                   raise
               time.sleep(2)
   ```

4. **Use more flexible selectors:**
   ```python
   # Instead of specific class names
   account_name = "//*[contains(@class, 'specific-class')]"
   
   # Use more general approaches
   account_name = "//span[contains(text(), '@')]"  # Find email-like text
   ```

---

### Issue: Login Failures

**Symptoms:**
- Login page loads but credentials aren't entered
- Authentication fails repeatedly
- Account gets locked or flagged

**Solutions:**

1. **Verify credentials manually:**
   ```bash
   # Test login manually in the same Chrome profile
   # Ensure 2FA is disabled or handled
   ```

2. **Check for CAPTCHA:**
   ```python
   def detect_captcha(driver):
       captcha_elements = [
           "//div[contains(@class, 'captcha')]",
           "//iframe[contains(@src, 'recaptcha')]",
           "//*[contains(text(), 'verify')]"
       ]
       
       for selector in captcha_elements:
           try:
               driver.find_element(By.XPATH, selector)
               return True
           except NoSuchElementException:
               continue
       return False
   ```

3. **Handle 2FA:**
   ```python
   def handle_2fa_prompt():
       print("2FA required. Please complete authentication manually.")
       input("Press Enter after completing 2FA...")
   ```

4. **Use session persistence:**
   ```python
   # Ensure Chrome profile saves login session
   # Login manually first, then run automation
   ```

---

## Installation Problems

### Python Version Issues

**Check Python version:**
```bash
python --version
# Should be 3.7 or higher
```

**Install correct Python version:**
```bash
# Using pyenv (recommended)
pyenv install 3.9.0
pyenv global 3.9.0

# Or download from python.org
```

### Virtual Environment Issues

**Create virtual environment:**
```bash
# Python 3.3+
python -m venv automation_env

# Activate
source automation_env/bin/activate  # Linux/macOS
automation_env\Scripts\activate     # Windows
```

**Fix common venv issues:**
```bash
# If venv is corrupted, recreate it
rm -rf automation_env
python -m venv automation_env
source automation_env/bin/activate
pip install -r requirements.txt
```

### Chrome/ChromeDriver Issues

**Symptoms:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Solutions:**

1. **Install ChromeDriver automatically:**
   ```bash
   pip install webdriver-manager
   ```
   
   ```python
   from webdriver_manager.chrome import ChromeDriverManager
   from selenium.webdriver.chrome.service import Service
   
   service = Service(ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service, options=chrome_options)
   ```

2. **Manual ChromeDriver installation:**
   ```bash
   # Download from https://chromedriver.chromium.org/
   # Extract to PATH or specify location
   ```

3. **Version compatibility:**
   ```bash
   # Check Chrome version
   google-chrome --version
   
   # Download matching ChromeDriver version
   ```

---

## Configuration Issues

### Credentials Not Loading

**Debug credential loading:**
```python
import os

# Check environment variables
print("FB_USERNAME:", os.getenv('FB_USERNAME', 'NOT_SET'))
print("FB_PASSWORD:", 'SET' if os.getenv('FB_PASSWORD') else 'NOT_SET')

# Check config file
try:
    with open('config.json') as f:
        config = json.load(f)
        print("Config loaded successfully")
except FileNotFoundError:
    print("Config file not found")
except json.JSONDecodeError:
    print("Invalid JSON in config file")
```

### Chrome Profile Configuration

**Debug profile path:**
```python
import os

profile_path = "C:/Users/YOUR_USERNAME/AppData/Local/Google/Chrome/User Data"
profile_dir = "Profile 4"

print(f"Profile path exists: {os.path.exists(profile_path)}")
print(f"Profile directory exists: {os.path.exists(os.path.join(profile_path, profile_dir))}")

# List available profiles
if os.path.exists(profile_path):
    profiles = [d for d in os.listdir(profile_path) if d.startswith('Profile') or d == 'Default']
    print(f"Available profiles: {profiles}")
```

### XPath Selector Issues

**Test XPath selectors:**
```python
def test_xpath_selector(driver, xpath, description):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        print(f"{description}: Found {len(elements)} elements")
        if elements:
            print(f"  First element text: {elements[0].text[:50]}...")
        return len(elements) > 0
    except Exception as e:
        print(f"{description}: Error - {e}")
        return False

# Test all selectors
test_xpath_selector(driver, dataMgr.account_name, "Account name")
test_xpath_selector(driver, dataMgr.account_icon, "Account icon")
```

---

## Runtime Errors

### Memory Issues

**Symptoms:**
- Browser crashes
- System becomes slow
- Out of memory errors

**Solutions:**
```python
# Optimize Chrome options for memory
chrome_options.add_argument("--memory-pressure-off")
chrome_options.add_argument("--max_old_space_size=4096")
chrome_options.add_argument("--disable-dev-shm-usage")

# Clean up resources
def cleanup_driver(driver):
    try:
        driver.quit()
    except:
        pass
    
    # Force cleanup
    import psutil
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            proc.kill()
```

### Network Timeouts

**Configure timeouts:**
```python
# Set various timeouts
driver.set_page_load_timeout(30)
driver.implicitly_wait(10)

# Custom timeout function
def wait_for_element(driver, xpath, timeout=30):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
```

### JavaScript Errors

**Debug JavaScript issues:**
```python
# Check for JavaScript errors
def check_js_errors(driver):
    logs = driver.get_log('browser')
    js_errors = [log for log in logs if log['level'] == 'SEVERE']
    
    if js_errors:
        print("JavaScript errors found:")
        for error in js_errors:
            print(f"  {error['message']}")
    
    return len(js_errors) == 0
```

---

## Performance Issues

### Slow Page Loading

**Optimize page loading:**
```python
# Disable images and CSS for speed
chrome_options.add_argument("--disable-images")
chrome_options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2
})

# Use headless mode
chrome_options.add_argument("--headless")
```

### Element Detection Delays

**Optimize element detection:**
```python
# Use shorter implicit waits with explicit waits
driver.implicitly_wait(2)  # Shorter default

# Smart wait function
def smart_wait_for_element(driver, xpath, timeout=10):
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            element = driver.find_element(By.XPATH, xpath)
            if element.is_displayed():
                return element
        except NoSuchElementException:
            pass
        
        time.sleep(0.5)
    
    raise TimeoutException(f"Element not found: {xpath}")
```

---

## Security & Detection Issues

### Automation Detection

**Symptoms:**
- Login challenges increase
- Account gets flagged
- Unusual security prompts

**Solutions:**

1. **Enhanced stealth mode:**
   ```python
   def setup_stealth_chrome():
       chrome_options = Options()
       
       # Remove automation indicators
       chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
       chrome_options.add_experimental_option('useAutomationExtension', False)
       chrome_options.add_argument("--disable-blink-features=AutomationControlled")
       
       # Mimic real user behavior
       chrome_options.add_argument("--disable-web-security")
       chrome_options.add_argument("--allow-running-insecure-content")
       
       # User agent spoofing
       chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
       
       return chrome_options
   ```

2. **Random delays:**
   ```python
   import random
   
   def human_like_delay():
       delay = random.uniform(1, 3)
       time.sleep(delay)
   
   def random_mouse_movement():
       # Implement random mouse movements
       pass
   ```

3. **Rate limiting:**
   ```python
   class RateLimiter:
       def __init__(self, actions_per_hour=100):
           self.actions_per_hour = actions_per_hour
           self.action_times = []
       
       def wait_if_needed(self):
           now = time.time()
           hour_ago = now - 3600
           
           # Remove old actions
           self.action_times = [t for t in self.action_times if t > hour_ago]
           
           if len(self.action_times) >= self.actions_per_hour:
               sleep_time = self.action_times[0] + 3600 - now
               time.sleep(sleep_time)
           
           self.action_times.append(now)
   ```

---

## Debugging Tools

### Enable Debug Logging

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation_debug.log'),
        logging.StreamHandler()
    ]
)

# Selenium logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.DEBUG)
```

### Screenshot Debugging

```python
def debug_screenshot(driver, step_name):
    """Take screenshot for debugging"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debug_{step_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Debug screenshot saved: {filename}")

def debug_page_source(driver, step_name):
    """Save page source for debugging"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debug_{step_name}_{timestamp}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f"Page source saved: {filename}")
```

### Element Inspector

```python
def inspect_element(driver, xpath):
    """Inspect element for debugging"""
    try:
        element = driver.find_element(By.XPATH, xpath)
        print(f"Element found: {xpath}")
        print(f"  Tag: {element.tag_name}")
        print(f"  Text: {element.text[:100]}...")
        print(f"  Visible: {element.is_displayed()}")
        print(f"  Enabled: {element.is_enabled()}")
        print(f"  Location: {element.location}")
        print(f"  Size: {element.size}")
        return element
    except NoSuchElementException:
        print(f"Element NOT found: {xpath}")
        
        # Try to find similar elements
        partial_xpath = xpath.split('/')[-1]  # Get last part
        try:
            similar = driver.find_elements(By.XPATH, f"//*[{partial_xpath}]")
            print(f"  Found {len(similar)} similar elements")
        except:
            pass
        
        return None
```

### Performance Profiling

```python
import cProfile
import pstats
from functools import wraps

def profile_function(func):
    """Decorator to profile function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return result
    return wrapper

# Usage
@profile_function
def perform_login(self):
    # Your login code here
    pass
```

---

## Getting Support

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing GitHub issues**
3. **Enable debug logging and gather logs**
4. **Try minimal reproduction case**
5. **Check Facebook's current UI for changes**

### Information to Include

When reporting issues, include:

```markdown
**Environment:**
- OS: [Windows 10/macOS/Ubuntu]
- Python version: [3.9.0]
- Chrome version: [91.0.4472.124]
- Selenium version: [4.0.0]

**Configuration:**
- Chrome profile path: [sanitized]
- Custom settings: [list any modifications]

**Error Details:**
- Full error message (sanitized)
- Log files (sanitized)
- Steps to reproduce

**What You've Tried:**
- List troubleshooting steps already attempted
- Any workarounds that partially work
```

### Creating Minimal Reproduction

```python
# Create simple test case that reproduces the issue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def minimal_test():
    chrome_options = Options()
    # Add minimal configuration
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Minimal steps to reproduce issue
        driver.get("https://facebook.com")
        # ... minimal reproduction steps
        
    except Exception as e:
        print(f"Error: {e}")
        # Take screenshot for debugging
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    minimal_test()
```

### Support Channels

1. **GitHub Issues**: For bugs and feature requests
2. **GitHub Discussions**: For questions and general help
3. **Documentation**: Check all documentation files first
4. **Stack Overflow**: Tag with `selenium` and `facebook-automation`

---

## Emergency Procedures

### Account Locked/Flagged

1. **Immediately stop automation**
2. **Login manually to check account status**
3. **Complete any security verification**
4. **Wait 24-48 hours before resuming**
5. **Implement additional stealth measures**

### Credential Compromise

1. **Change Facebook password immediately**
2. **Enable 2FA if not already enabled**
3. **Review account activity**
4. **Update stored credentials**
5. **Audit code for credential exposure**

### System Compromise

1. **Stop all automation processes**
2. **Scan system for malware**
3. **Change all passwords**
4. **Review system logs**
5. **Update security measures**

---

Remember: This tool is for educational purposes. Always comply with Facebook's Terms of Service and applicable laws.