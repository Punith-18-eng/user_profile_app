# Contributing to Text Classification with TensorFlow

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## 🤝 Ways to Contribute

1. **Report Bugs** - File issues for bugs you find
2. **Suggest Features** - Propose new features or improvements
3. **Submit Code** - Send pull requests with bug fixes or features
4. **Improve Docs** - Help improve documentation
5. **Share Examples** - Contribute usage examples or integration guides

## 🐛 Reporting Bugs

### Before Submitting
- Check if the issue already exists
- Verify it's reproducible
- Gather information about your environment

### When Submitting
Include:
- Clear, descriptive title
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant code snippets or logs

Example:
```
Title: Model fails to load on Windows
Description: When using flask_app.py on Windows, the model fails to load...
Steps:
1. Run `python flask_app.py`
2. Make POST request to /predict
Expected: Prediction returned
Actual: FileNotFoundError
Environment: Windows 10, Python 3.10, TensorFlow 2.10.0
```

## 💡 Suggesting Features

- Use clear, descriptive title
- Explain the motivation and use case
- Provide examples if applicable
- Note related issues or features

## 🔧 Setting Up Development Environment

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/user_profile_app.git
cd Text_Classification_Project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies
```bash
pip install -r requirements_deployment.txt
pip install -r requirements-dev.txt
```

### 4. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Code Style Guidelines

### Python Style (PEP 8)
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions

### Formatting
```bash
# Format code with Black
black . --line-length 100

# Check code style with Flake8
flake8 . --max-line-length 100

# Type checking with mypy
mypy flask_app.py streamlit_app.py --ignore-missing-imports
```

### Example Function
```python
def clean_text(text: str, remove_stopwords: bool = True) -> str:
    """
    Clean and preprocess text for classification.
    
    Args:
        text: Input text to clean
        remove_stopwords: Whether to remove stopwords (default: True)
    
    Returns:
        Cleaned text string
    
    Example:
        >>> clean_text("Hello, World!!!")
        'hello world'
    """
    # Implementation here
    pass
```

## ✅ Testing Guidelines

### Run Tests
```bash
# Run test suite
python test_api.py

# Run specific tests
pytest test_api.py -v

# Run with coverage
pytest test_api.py --cov=flask_app
```

### Writing Tests
```python
import unittest
from unittest.mock import patch

class TestClassification(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_predict_valid_text(self):
        """Test prediction with valid input"""
        # Arrange
        text = "Sample text"
        
        # Act
        result = predict(text)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIn('prediction', result)
```

### Testing Requirements
- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage for new code

## 🔄 Submitting Pull Requests

### Before Submitting
1. **Sync with main branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run tests**
   ```bash
   python test_api.py
   ```

3. **Format code**
   ```bash
   black .
   flake8 .
   ```

4. **Update documentation** if needed

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #ISSUE_NUMBER

## Changes
- Change 1
- Change 2

## Testing
- [ ] Added tests
- [ ] All tests pass
- [ ] Tested locally

## Screenshots (if applicable)
```

### PR Review Process
1. Automated checks run (linting, tests)
2. Code review by maintainers
3. Requested changes addressed
4. Merge when approved

## 📚 Documentation

### Writing Docs
- Use Markdown format
- Include code examples
- Keep language clear and simple
- Update table of contents if adding sections

### Docstring Format
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description.
    
    Longer description explaining the function in detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: Description of when raised
    
    Example:
        >>> result = function_name('arg1', 'arg2')
        >>> print(result)
        expected_output
    """
```

## 🚀 Deployment & Release

### Version Numbering
- Use Semantic Versioning: MAJOR.MINOR.PATCH
- Examples: 1.0.0, 1.2.3, 2.0.0-beta.1

### Release Process
1. Update CHANGELOG.md
2. Bump version in setup.py/pyproject.toml
3. Create release tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub Release with notes

## 🔐 Security Guidelines

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive data
- Keep dependencies updated
- Report security issues privately to maintainers

## 📋 Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Test addition
- `chore`: Build/dependency updates

### Example
```
feat(api): add batch prediction endpoint

Add support for predicting multiple texts in a single request.
Includes validation for max 1000 texts per request.

Closes #123
```

## 🏆 Code of Conduct

- Be respectful and inclusive
- Avoid harassment or discrimination
- Constructive criticism only
- Respect others' work and ideas

## 📞 Getting Help

- Check existing issues and discussions
- Review documentation in QUICKSTART.md, DEPLOYMENT.md
- Ask questions in issue comments
- Contact maintainers if needed

## 🎯 Development Priorities

1. Bug fixes for reported issues
2. Improvements to core functionality
3. Documentation enhancements
4. New features (discussed in issues first)

## 📊 Project Metrics

We track:
- Code coverage (aim for >80%)
- Test pass rate (should be 100%)
- Performance benchmarks
- User feedback and issues

## 🔄 Feedback Loop

After submitting a PR:
- Expect review within 48-72 hours
- Respond to comments/suggestions
- Make requested changes
- Thank you for contributing!

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's license.

## 🙏 Acknowledgments

Contributors will be recognized in:
- CONTRIBUTORS.md
- Release notes
- GitHub contributors page

---

**Thank you for contributing to make this project better! 🎉**
