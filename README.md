# AI-Powered Python Project Template

A comprehensive template for Python projects that leverage AI as the main programmer, featuring modern development practices and comprehensive tooling.

## Project Structure

```
.
├── src/                    # Source code
│   ├── __init__.py
│   ├── core/              # Core functionality
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic and services
│   ├── utils/             # Utility functions
│   └── config/            # Configuration management
├── tests/                 # Test files
│   ├── __init__.py
│   ├── conftest.py       # Test configuration
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                  # Documentation
│   ├── api/              # API documentation
│   ├── guides/           # User guides
│   └── examples/         # Example notebooks
├── scripts/              # Utility scripts
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── pyproject.toml       # Project configuration and dependencies
└── README.md            # This file
```

## Features

- Modern Python packaging with `pyproject.toml`
- Type checking with `mypy`
- Code formatting with `black` and `isort`
- Linting with `ruff`
- Testing with `pytest` and coverage reporting
- Pre-commit hooks for code quality
- FastAPI for API development
- OpenAI integration ready
- Environment variable management with `python-dotenv`
- Comprehensive documentation with Sphinx
- CI/CD templates for GitHub Actions
- Security scanning with Bandit
- Code coverage reporting
- Automated dependency updates

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- git
- pre-commit (optional but recommended)

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable and function names
- Comment complex logic, not obvious code

### Testing

- Write unit tests for all new features
- Maintain test coverage above 80%
- Use appropriate test markers (unit, integration, slow)
- Run tests before committing:
  ```bash
  pytest
  ```

### Documentation

- Keep documentation up to date
- Use clear and concise language
- Include examples where appropriate
- Document API endpoints with OpenAPI/Swagger
- Build documentation locally:
  ```bash
  cd docs
  make html
  ```

### Git Workflow

1. Create a new branch for each feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. Push your changes:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request

### Commit Messages

Follow the Conventional Commits specification:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test updates
- `chore:` Maintenance tasks

## CI/CD

The project includes GitHub Actions workflows for:
- Code quality checks
- Testing
- Documentation building
- Dependency updates
- Security scanning
- Release management

## Security

- Never commit sensitive information
- Use environment variables for secrets
- Regular security audits with Bandit
- Keep dependencies updated
- Follow security best practices

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 