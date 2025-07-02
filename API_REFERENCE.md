# API Reference

This document provides detailed API documentation for all classes and methods in the Python Facebook Page Automation project.

## Table of Contents

- [ApplicationController](#applicationcontroller)
- [AuthenticationManager](#authenticationmanager)
- [SeleniumManager](#seleniummanager)
- [ConfigManager](#configmanager)
- [DataManager](#datamanager)
- [Placeholder Classes](#placeholder-classes)

---

## ApplicationController

**File**: `fb_atumation.py`

The main controller class that orchestrates the entire automation workflow.

### Class Definition

```python
class ApplicationController:
    """
    A controller class to encapsulate the flow:
        - Initialize WebDriver and managers.
        - Perform login.
        - Navigate account UI.
        - Retrieve pages container and filter pages.
    """
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `driverManager` | SeleniumManager | Manages WebDriver instance and interactions |
| `webdriver` | WebDriver | Selenium WebDriver instance |
| `username` | str | Facebook login username |
| `password` | str | Facebook login password |
| `authMang` | AuthenticationManager | Handles login authentication |
| `dataMgr` | DataManager | Manages XPath selectors and data |
| `confgMgr` | ConfigManager | Manages configuration and page filtering |

### Methods

#### `__init__()`

Initializes the ApplicationController with all necessary components.

**Parameters**: None

**Returns**: None

**Example**:
```python
app = ApplicationController()
```

**Behavior**:
- Initializes SeleniumManager and WebDriver
- Sets up login credentials (⚠️ currently hardcoded)
- Creates instances of all manager classes

---

#### `login()`

Executes the login sequence using AuthenticationManager.

**Parameters**: None

**Returns**: `bool` - True if login successful, False otherwise

**Example**:
```python
success = app.login()
if success:
    print("Login successful")
```

**Behavior**:
- Opens Facebook login page
- Detects login form elements
- Performs automated login
- Handles exceptions and returns status

---

#### `setup_account_ui()`

Performs UI actions to reveal the account pages container.

**Parameters**: None

**Returns**: None

**Example**:
```python
app.setup_account_ui()
```

**Behavior**:
- Retrieves current account name
- Clicks account icon
- Navigates to all profiles view
- Updates ConfigManager with current account

---

#### `retrieve_account_pages()`

Retrieves and processes account pages using ConfigManager.

**Parameters**: None

**Returns**: None

**Example**:
```python
app.retrieve_account_pages()
```

**Behavior**:
- Finds pages container element
- Filters and processes pages
- Updates DataManager with results

---

#### `run()`

Executes the complete automation workflow.

**Parameters**: None

**Returns**: None

**Example**:
```python
app = ApplicationController()
app.run()
```

**Behavior**:
- Performs login
- Sets up account UI
- Retrieves account pages
- Includes debug delay (sleep)

---

## AuthenticationManager

**File**: `auth.py`

Manages Facebook login authentication using Selenium WebDriver.

### Class Definition

```python
class AuthenticationManager:
    """
    Manages login authentication using Selenium WebDriver.
    """
```

### Private Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `__wdriver` | WebDriver | WebDriver instance |
| `__driverManager` | SeleniumManager | SeleniumManager instance |
| `__username` | str | Login username |
| `__password` | str | Login password |
| `__input_email` | WebElement | Email input element |
| `__input_pass` | WebElement | Password input element |
| `__login_button` | WebElement | Login button element |
| `__login_url` | str | Facebook login URL |

### Methods

#### `__init__(driverManager, username, password)`

Initializes AuthenticationManager with required components.

**Parameters**:
- `driverManager` (SeleniumManager): Provides WebDriver instance
- `username` (str): Username for authentication
- `password` (str): Password for authentication

**Returns**: None

**Example**:
```python
auth = AuthenticationManager(driver_manager, "user@example.com", "password")
```

---

#### `open_login_page()`

Opens the Facebook login page and waits for it to load.

**Parameters**: None

**Returns**: None

**Example**:
```python
auth.open_login_page()
```

**Behavior**:
- Navigates to Facebook login URL
- Waits 10 seconds for page load (⚠️ uses sleep)

---

#### `detect_login_page()`

Detects if essential login elements are present on the page.

**Parameters**: None

**Returns**: `bool` - True if login elements found, False otherwise

**Example**:
```python
if auth.detect_login_page():
    print("Login page detected")
```

**Behavior**:
- Locates email input field (name="email")
- Locates password input field (name="pass")
- Locates login button (name="login")
- Returns True if all elements found

---

#### `_clear_fields()`

Private method to clear any pre-filled data in login fields.

**Parameters**: None

**Returns**: None

**Behavior**:
- Sends dummy text to fields
- Clears both email and password fields

---

#### `preform_login()`

Performs the automated login process by simulating user interactions.

**Parameters**: None

**Returns**: `bool` - True if login steps executed successfully, False otherwise

**Example**:
```python
success = auth.preform_login()
```

**Behavior**:
- Clears existing field content
- Navigates to email field using SeleniumManager
- Enters username
- Navigates to login button
- Enters password
- Clicks to submit form

---

## SeleniumManager

**File**: `integration.py`

Handles WebDriver management and provides enhanced interaction methods.

### Class Definition

```python
class SeleniumManager:
```

### Private Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `__wdriver` | WebDriver | Chrome WebDriver instance |

### Methods

#### `Initialze_webdriver()`

Note: Method name has typo (should be "Initialize")

Initializes Chrome WebDriver with stealth and profile options.

**Parameters**: None

**Returns**: None

**Example**:
```python
manager = SeleniumManager()
manager.Initialze_webdriver()
```

**Behavior**:
- Configures Chrome options for stealth mode
- Sets up Chrome user profile (Windows-specific path)
- Maximizes browser window
- Disables automation detection features

**Chrome Options Applied**:
- `useAutomationExtension: false`
- `excludeSwitches: ["enable-automation"]`
- `--disable-blink-features=AutomationControlled`
- Custom user data directory and profile

---

#### `get_webdriver()`

Returns the initialized WebDriver instance.

**Parameters**: None

**Returns**: `WebDriver` - Chrome WebDriver instance

**Example**:
```python
driver = manager.get_webdriver()
```

---

#### `navigate_to_elem(element, min_coordinate=10, movement_duration=1)`

Moves mouse cursor to the center of a specified element naturally.

**Parameters**:
- `element` (WebElement): Target element for navigation
- `min_coordinate` (int, optional): Minimum coordinate value (default: 10)
- `movement_duration` (float, optional): Duration of mouse movement (default: 1)

**Returns**: None

**Example**:
```python
element = driver.find_element(By.ID, "submit")
manager.navigate_to_elem(element, movement_duration=2)
```

**Behavior**:
- Calculates element's absolute screen position
- Accounts for browser window position and offsets
- Uses PyAutoGUI to move mouse naturally
- Ensures coordinates are within screen bounds

---

#### `clickOnScreen()`

Performs a mouse click at the current cursor position.

**Parameters**: None

**Returns**: None

**Example**:
```python
manager.navigate_to_elem(element)
manager.clickOnScreen()
```

**Behavior**:
- Uses PyAutoGUI to perform mouse click
- Clicks at current cursor position

---

## ConfigManager

**File**: `config.py`

Manages configuration and page filtering logic.

### Class Definition

```python
class ConfigManager:
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `currentAccount` | str | Current account being processed |
| `PagesOnAccount` | WebElement | Container element holding all pages |
| `mainPage` | str | Main page name for filtering |
| `dataMgr` | DataManager | DataManager instance |

### Methods

#### `__init__(main_page="", current_account="", pages_on_account=None)`

Initializes ConfigManager with configuration values.

**Parameters**:
- `main_page` (str, optional): Main page name
- `current_account` (str, optional): Current account name
- `pages_on_account` (WebElement, optional): Pages container element

**Returns**: None

**Example**:
```python
config = ConfigManager(main_page="My Main Page")
```

---

#### `getAccountPages(cAccount="", unorgnizedElements=None)`

Processes unorganized element container to retrieve account pages.

**Parameters**:
- `cAccount` (str, optional): Account name (uses currentAccount if empty)
- `unorgnizedElements` (WebElement, optional): Container element (uses PagesOnAccount if None)

**Returns**: `List[WebElement]` - Filtered list of page elements

**Example**:
```python
pages = config.getAccountPages()
print(f"Found {len(pages)} pages")
```

**Behavior**:
- Uses provided or stored account and container
- Finds page elements using XPath selector
- Applies filtering logic based on account type
- Returns organized list of page elements

---

#### `_filter_pages(pages, cAccount, skip_last)`

Private method that filters page elements based on common rules.

**Parameters**:
- `pages` (List[WebElement]): List of page elements to filter
- `cAccount` (str): Account name for filtering
- `skip_last` (bool): Whether to skip the last element

**Returns**: `List[WebElement]` - Filtered list of page elements

**Behavior**:
- Filters out empty text and account name matches
- Optionally skips last element for main accounts
- Handles exceptions during text extraction

---

## DataManager

**File**: `config.py`

Manages XPath selectors and data storage for Facebook elements.

### Class Definition

```python
class DataManager:
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `mainPage` | str | Main page name |
| `account_name` | str | XPath for account name element |
| `create_page_button` | str | XPath for create page button |
| `account_icon` | str | XPath for account icon |
| `all_profiles_button` | str | XPath for all profiles button |
| `pages_containter` | str | XPath for pages container |
| `pages_filter` | str | XPath for individual page elements |
| `account_pages` | list[str] | List of account page names |

### XPath Selectors

#### Account Elements
```python
account_name = "//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']"
account_icon = "//*[local-name()='g' and @mask='url(#«R1ldm6l6ismipapd5aq»)']"
```

#### Navigation Elements
```python
all_profiles_button = "//*[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f x1dem4cn')]//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft']"
```

#### Page Elements
```python
pages_containter = "//div[contains(@class,'x78zum5 xdt5ytf')]//div[contains(@class,'xwxc41k x1y1aw1k')]/div[@class='html-div x11i5rnm x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1oo3vh0 x1rdy4ex' and @role='list']"

pages_filter = "//div[@role='listitem']//*[contains(@class,'x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli xz9dl7a xsag5q8 x4uap5 xkhd6sd x1n2onr6 x1ja2u2z')]//div[@class='x78zum5 xdt5ytf xz62fqu x16ldp7u']/div[@class='xu06os2 x1ok221b']/span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h']"
```

---

## Placeholder Classes

The following classes are currently placeholders for future functionality:

### ContentUploader (`upload.py`)
```python
class ContentUploader:
    pass
```
**Purpose**: Future implementation for content upload automation.

### PostAutomation (`post_automation.py`)
```python
class PostAutomation:
    pass
```
**Purpose**: Future implementation for post scheduling and management.

### GroupRetrieval (`retrieval.py`)
```python
class GroupRetrieval:
    pass
```
**Purpose**: Future implementation for content retrieval and data extraction.

### CleanupManager (`cleanup.py`)
```python
class CleanupManager:
    pass
```
**Purpose**: Future implementation for cleanup and maintenance tasks.

---

## Error Handling Patterns

### Common Exception Handling
Most methods follow this pattern:
```python
try:
    # Main logic
    return success_value
except Exception as e:
    print(f"Error message: {e}")
    return failure_value
```

### Recommended Improvements
- Use specific exception types instead of generic Exception
- Implement proper logging instead of print statements
- Add retry mechanisms for transient failures
- Validate input parameters

---

## Type Hints and Annotations

The codebase uses Python type hints in several places:
- `WebElement` from selenium.webdriver.remote.webelement
- `WebDriver` from selenium.webdriver.chrome.webdriver
- `List` from typing module
- Return type annotations for methods

### Recommended Improvements
- Add complete type hints to all method parameters
- Use Optional[] for parameters that can be None
- Add Union[] types where multiple types are accepted
- Consider using dataclasses for configuration objects