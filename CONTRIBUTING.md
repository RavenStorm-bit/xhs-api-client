# Contributing to XHS API Client

We welcome contributions to the XHS API Client! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Describe the issue clearly with steps to reproduce
- Include error messages and logs if applicable

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add some feature'`)
7. Push to the branch (`git push origin feature/your-feature`)
8. Create a Pull Request

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Testing
- Write tests for new features
- Ensure existing tests pass
- Test with different Python versions (3.7+)

## Development Setup

```bash
# Clone the repository
git clone https://github.com/RavenStorm-bit/xhs-api-client.git
cd xhs-api-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

## Important Notes

### Token Server
This client requires a token generation server. The server implementation is not included in this repository for security reasons. Contributors should:
- Focus on client-side improvements
- Not attempt to reverse-engineer token generation
- Test with a mock server or provided test server

### Security
- Never commit real API keys or cookies
- Use example/mock data in tests
- Report security issues privately to maintainers

## Questions?
Feel free to open an issue for any questions about contributing!