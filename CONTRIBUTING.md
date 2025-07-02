# Contributing to Python Facebook Page Automation

Thank you for your interest in contributing to this project! This guide will help you understand how to contribute effectively.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Standards](#code-standards)
- [Contribution Types](#contribution-types)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Security Guidelines](#security-guidelines)
- [Community Guidelines](#community-guidelines)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.7 or higher
- Git for version control
- Basic understanding of web automation
- Familiarity with Selenium WebDriver
- Understanding of Facebook's UI structure

### First-Time Setup

1. **Fork the Repository**
   ```bash
   # Click 'Fork' on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/PythonPageAutomation.git
   cd PythonPageAutomation
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pytest black flake8 mypy
   ```

3. **Configure Development Settings**
   ```bash
   # Copy example configuration
   cp config.example.json config.json
   
   # Edit with your development settings
   nano config.json
   ```

---

## Development Environment

### Directory Structure

```
PythonPageAutomation/
├── src/
│   ├── fb_atumation.py      # Main application
│   ├── auth.py              # Authentication
│   ├── integration.py       # WebDriver integration
│   └── config.py           # Configuration
├── tests/
│   ├── test_auth.py
│   ├── test_integration.py
│   └── test_config.py
├── docs/
│   ├── README.md
│   ├── API_REFERENCE.md
│   └── SECURITY.md
├── requirements.txt
├── requirements-dev.txt
└── setup.py
```

### Development Tools

#### Code Formatting
```bash
# Format code with Black
black *.py

# Check formatting
black --check *.py
```

#### Linting
```bash
# Run flake8 linter
flake8 *.py

# Run mypy type checker
mypy *.py
```

#### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_auth.py
```

---

## Code Standards

### Python Style Guide

We follow PEP 8 with these specific guidelines:

#### Naming Conventions
```python
# Classes: PascalCase
class AuthenticationManager:
    pass

# Functions and variables: snake_case
def perform_login():
    user_name = "example"

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3

# Private methods: _leading_underscore
def _clear_fields(self):
    pass
```

#### Type Hints
```python
# Always include type hints for function parameters and return values
def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user with Facebook."""
    return True

# Use Optional for parameters that can be None
from typing import Optional, List
def get_pages(account: Optional[str] = None) -> List[str]:
    return []
```

#### Docstrings
```python
def perform_login(self, username: str, password: str) -> bool:
    """
    Perform automated login to Facebook.
    
    Args:
        username: Facebook email or username
        password: Account password
        
    Returns:
        True if login successful, False otherwise
        
    Raises:
        AuthenticationError: When login credentials are invalid
        NetworkError: When network connectivity issues occur
        
    Example:
        >>> auth = AuthenticationManager()
        >>> success = auth.perform_login("user@example.com", "password")
        >>> print(success)
        True
    """
    pass
```

### Security Standards

#### Never Commit Sensitive Data
```python
# ❌ BAD - Never do this
username = "real_email@example.com"
password = "real_password"

# ✅ GOOD - Use environment variables or config files
import os
username = os.getenv('FB_USERNAME')
password = os.getenv('FB_PASSWORD')
```

#### Secure Error Handling
```python
# ❌ BAD - Exposes sensitive information
except Exception as e:
    print(f"Login failed with {username} and {password}: {e}")

# ✅ GOOD - Sanitized error messages
except Exception as e:
    logger.error(f"Login failed for user {username[:3]}***@***: {str(e)}")
```

### Code Organization

#### Import Organization
```python
# Standard library imports
import os
import time
from typing import List, Optional

# Third-party imports
from selenium import webdriver
from selenium.webdriver.common.by import By

# Local imports
from .config import DataManager
from .auth import AuthenticationManager
```

#### Class Structure
```python
class ExampleClass:
    """Class docstring explaining purpose."""
    
    def __init__(self, param: str):
        """Initialize with parameters."""
        self.param = param
        self._private_attr = None
    
    @property
    def public_property(self) -> str:
        """Public property with docstring."""
        return self._private_attr
    
    def public_method(self) -> bool:
        """Public method implementation."""
        return self._private_method()
    
    def _private_method(self) -> bool:
        """Private method for internal use."""
        return True
```

---

## Contribution Types

### Bug Fixes

#### Bug Report Requirements
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, browser version)
- Relevant log outputs (sanitized)

#### Bug Fix Process
1. Create issue describing the bug
2. Create branch: `git checkout -b fix/issue-123-login-failure`
3. Write test that reproduces the bug
4. Implement fix
5. Ensure test passes
6. Submit pull request

### Feature Additions

#### Feature Request Guidelines
- Describe the use case and benefit
- Provide examples of how it would be used
- Consider impact on existing functionality
- Discuss implementation approach

#### Feature Development Process
1. Discuss feature in GitHub issue first
2. Create branch: `git checkout -b feature/page-content-upload`
3. Implement feature with tests
4. Update documentation
5. Submit pull request

### Documentation Improvements

#### Types of Documentation
- Code comments and docstrings
- README and setup guides
- API reference documentation
- Security and best practices
- Troubleshooting guides

#### Documentation Standards
- Write clear, concise explanations
- Include practical examples
- Keep documentation up-to-date with code changes
- Use proper markdown formatting

### Performance Improvements

#### Performance Guidelines
- Profile code before optimizing
- Focus on actual bottlenecks
- Maintain code readability
- Add performance tests
- Document performance considerations

---

## Pull Request Process

### Before Submitting

1. **Run Full Test Suite**
   ```bash
   # Run all tests
   pytest tests/
   
   # Check code formatting
   black --check *.py
   flake8 *.py
   mypy *.py
   ```

2. **Update Documentation**
   - Update relevant docstrings
   - Add or update README sections
   - Update API reference if needed

3. **Test Manually**
   - Test with real Facebook account (if safe)
   - Verify no regression in existing features
   - Test edge cases and error conditions

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Manual testing completed
- [ ] Added tests for new functionality

## Security
- [ ] No sensitive data exposed
- [ ] Security implications considered
- [ ] Follows security best practices

## Documentation
- [ ] Code comments updated
- [ ] README updated (if needed)
- [ ] API documentation updated (if needed)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Changes tested thoroughly
- [ ] Documentation is clear and complete
```

### Review Process

1. **Automated Checks**
   - GitHub Actions will run tests
   - Code quality checks will run
   - Security scans will be performed

2. **Manual Review**
   - Code review by maintainers
   - Security review for sensitive changes
   - Documentation review

3. **Approval and Merge**
   - Requires approval from maintainers
   - All checks must pass
   - Branch will be merged using squash merge

---

## Issue Reporting

### Bug Reports

Use this template for bug reports:

```markdown
**Bug Description**
Clear description of what went wrong

**To Reproduce**
Steps to reproduce the behavior:
1. Configure automation with...
2. Run the script...
3. See error...

**Expected Behavior**
What should have happened

**Screenshots/Logs**
If applicable, add sanitized logs or screenshots

**Environment:**
- OS: [e.g. Windows 10]
- Python Version: [e.g. 3.9]
- Chrome Version: [e.g. 91.0.4472.124]
- Dependencies: [run `pip freeze`]

**Additional Context**
Any other relevant information
```

### Feature Requests

Use this template for feature requests:

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Explain why this feature would be useful

**Proposed Implementation**
If you have ideas about how to implement this

**Alternatives Considered**
Other ways to achieve the same goal

**Additional Context**
Any other relevant information
```

### Security Issues

**Do not** report security issues in public GitHub issues. Instead:
1. Email security issues to [maintainer email]
2. Include detailed description and reproduction steps
3. Allow time for assessment and fix before public disclosure

---

## Security Guidelines

### Development Security

#### Credential Handling
```python
# ✅ GOOD - Use environment variables
import os
username = os.getenv('FB_USERNAME')

# ✅ GOOD - Use configuration files (not in git)
with open('config.json') as f:
    config = json.load(f)
    username = config['username']

# ❌ BAD - Never hardcode credentials
username = "actual_email@example.com"
```

#### Logging Security
```python
# ✅ GOOD - Sanitized logging
logger.info(f"Login attempt for user: {username[:3]}***")

# ❌ BAD - Exposing sensitive data
logger.info(f"Login with {username} and {password}")
```

### Testing Security

#### Test Data
```python
# Use dummy/fake data for tests
TEST_USERNAME = "test_user@example.com"
TEST_PASSWORD = "fake_password"

# Never use real credentials in tests
def test_login():
    auth = AuthenticationManager()
    # Mock the login instead of using real credentials
    with mock.patch.object(auth, 'perform_login') as mock_login:
        mock_login.return_value = True
        result = auth.perform_login(TEST_USERNAME, TEST_PASSWORD)
        assert result is True
```

---

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors.

#### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Harassment or discriminatory language
- Trolling, insulting, or derogatory comments
- Public or private harassment
- Publishing others' private information without consent
- Other conduct which could reasonably be considered inappropriate

#### Enforcement

Community guidelines are enforced by project maintainers. Unacceptable behavior may result in:
- Warning
- Temporary ban from project repositories
- Permanent ban from project repositories

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Pull Requests**: Code contributions, reviews
- **Email**: Security issues, private communications

---

## Development Roadmap

### Short-term Goals (Next 3 months)
- [ ] Implement secure credential management
- [ ] Add comprehensive error handling
- [ ] Create test suite with good coverage
- [ ] Improve XPath selector resilience
- [ ] Add configuration file support

### Medium-term Goals (3-6 months)
- [ ] Implement content upload functionality
- [ ] Add post automation features
- [ ] Create web interface for configuration
- [ ] Add support for multiple accounts
- [ ] Implement headless browser support

### Long-term Goals (6+ months)
- [ ] Cross-platform support (macOS, Linux)
- [ ] Plugin architecture for extensibility
- [ ] Advanced analytics and reporting
- [ ] Machine learning for better element detection
- [ ] Enterprise features and deployment options

---

## Getting Help

### Documentation
- Read the [README](README.md) for basic usage
- Check the [API Reference](API_REFERENCE.md) for detailed documentation
- Review [Security Guidelines](SECURITY.md) for security best practices

### Community Support
- Search existing GitHub issues
- Ask questions in GitHub Discussions
- Join community chat (if available)

### Maintainer Contact
- Create GitHub issue for bugs or features
- Email security issues privately
- Tag maintainers in urgent issues

---

## Recognition

Contributors will be recognized in the following ways:
- Listed in CONTRIBUTORS.md file
- Mentioned in release notes for significant contributions
- Given collaborator access for consistent high-quality contributions

Thank you for contributing to Python Facebook Page Automation! 🎉