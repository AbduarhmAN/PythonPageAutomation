# PythonPageAutomation Test Suite

This repository contains a comprehensive test suite for the Facebook page automation project.

## Project Overview

This is a Selenium-based web automation tool for Facebook page management with the following main components:

- **ApplicationController** (`fb_atumation.py`) - Main orchestrator for the automation flow
- **SeleniumManager** (`integration.py`) - WebDriver management and screen interaction utilities  
- **AuthenticationManager** (`auth.py`) - Facebook login automation
- **DataManager & ConfigManager** (`config.py`) - XPath selector management and page filtering logic
- **Stub classes** - Placeholder classes for future functionality (cleanup, post automation, retrieval, upload)

## Test Structure

### Test Files

1. **Unit Tests with Mocking** (`tests/` directory):
   - `test_config.py` - Tests for DataManager and ConfigManager classes
   - `test_integration.py` - Tests for SeleniumManager class
   - `test_auth.py` - Tests for AuthenticationManager class
   - `test_fb_automation.py` - Tests for ApplicationController class
   - `test_stub_classes.py` - Tests for stub classes

2. **Standalone Tests** (`simple_test.py`):
   - Basic structure validation
   - XPath pattern validation
   - Application logic tests
   - File existence checks

### Dependencies

The project requires the following dependencies (listed in `requirements.txt`):
- `selenium>=4.0.0` - Web automation framework
- `pyautogui>=0.9.0` - Screen automation utilities

### Running Tests

#### Option 1: Simple Validation Tests (No Dependencies Required)
```bash
python3 simple_test.py
```

This runs basic structure and logic validation tests that don't require external dependencies.

#### Option 2: Full Unit Test Suite (Requires Dependencies)
```bash
# Install dependencies first
pip install -r requirements.txt

# Run all unit tests
python3 -m unittest discover tests -v

# Or use the test runner script
python3 run_tests.py
```

#### Option 3: Individual Test Files
```bash
python3 -m unittest tests.test_config -v
python3 -m unittest tests.test_integration -v  
python3 -m unittest tests.test_auth -v
python3 -m unittest tests.test_fb_automation -v
python3 -m unittest tests.test_stub_classes -v
```

## Test Coverage

### What's Tested

1. **Configuration Management**:
   - DataManager initialization and XPath selectors
   - ConfigManager page filtering logic
   - Error handling for invalid elements

2. **Selenium Integration**:
   - WebDriver initialization with Chrome options
   - Element navigation and coordinate calculation
   - Screen clicking functionality
   - Boundary condition handling

3. **Authentication Flow**:
   - Login page detection
   - Field clearing and credential entry
   - Error handling for missing elements

4. **Application Flow**:
   - Complete automation workflow
   - UI setup and page retrieval
   - Exception handling throughout the flow

5. **Project Structure**:
   - File existence validation
   - Import capability testing
   - Requirements and configuration validation

### Testing Approach

- **Mocking**: External dependencies (Selenium WebDriver, pyautogui) are mocked to test logic without browser automation
- **Unit Testing**: Each class is tested in isolation with comprehensive scenarios
- **Integration Testing**: Application flow is tested end-to-end with mocked dependencies
- **Structure Testing**: Project organization and file structure are validated

## Test Results

The test suite includes:
- **60+ individual test cases** covering all major functionality
- **Error handling scenarios** for network issues, missing elements, etc.
- **Edge case testing** for boundary conditions and invalid inputs
- **Mock-based testing** to avoid actual browser automation during testing

## Key Features Tested

1. **Facebook Login Automation**:
   - Credential management
   - Element detection and interaction
   - Error recovery

2. **Page Management**:
   - Account page retrieval and filtering
   - XPath selector validation
   - Element processing logic

3. **Browser Integration**:
   - Chrome WebDriver configuration
   - Window and coordinate management
   - Screen interaction utilities

4. **Configuration Management**:
   - XPath selector organization
   - Page filtering algorithms
   - Account-specific logic

## Development Notes

- Tests use extensive mocking to avoid requiring actual Chrome browser or Facebook access
- All hardcoded credentials are test-safe (publicly visible in code)
- XPath selectors are validated for basic structure but not functionality
- Sleep patterns are tested for reasonableness but not actual timing

## Future Enhancements

The test suite is designed to be easily extended when the stub classes are implemented:
- Add tests for CleanupManager functionality
- Add tests for PostAutomation features  
- Add tests for GroupRetrieval capabilities
- Add tests for ContentUploader operations

## Running in CI/CD

The `simple_test.py` file is ideal for CI/CD environments as it requires no external dependencies and validates the basic project structure and logic patterns.