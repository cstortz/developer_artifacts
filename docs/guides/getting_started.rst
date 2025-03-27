Getting Started
==============

This guide will help you get started with the AI-Powered Project template.

Prerequisites
------------

* Python 3.11 or higher
* pip (Python package installer)
* git
* pre-commit (optional but recommended)

Project Structure
---------------

The project follows a modern Python project structure:

.. code-block:: text

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
   └── README.md            # Project documentation

Create the directory structure:
.. code-block:: bash

   # Create main directories
   mkdir -p src/{api,core,db,models,services,utils} tests/{unit,integration,e2e} docs/{api,guides} .github/workflows

   # Create Python package files
   touch src/__init__.py src/api/__init__.py src/core/__init__.py src/db/__init__.py src/models/__init__.py src/services/__init__.py src/utils/__init__.py tests/__init__.py tests/unit/__init__.py tests/integration/__init__.py tests/e2e/__init__.py

   # Create main application files
   touch src/main.py src/api/endpoints.py src/core/config.py src/db/session.py src/models/base.py src/services/ai.py src/utils/security.py

Setup
-----

1. Clone the repository:
   .. code-block:: bash

      git clone <your-repository-url>
      cd <repository-name>

2. Create and activate a virtual environment:
   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies:
   .. code-block:: bash

      pip install -e ".[dev]"

4. Set up pre-commit hooks:
   .. code-block:: bash

      pre-commit install

5. Copy `.env.example` to `.env` and configure your environment variables:
   .. code-block:: bash

      cp .env.example .env

Logging Configuration
------------------

The project includes a comprehensive logging configuration that supports both console and file logging:

1. Configure logging in your `.env` file:
   .. code-block:: text

      LOG_LEVEL=INFO
      LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
      LOG_FILE=logs/app.log

2. Import and use the logger in your code:
   .. code-block:: python

      from src.core.logging import get_logger

      logger = get_logger(__name__)

      def your_function():
          logger.info("Starting operation")
          try:
              # Your code here
              logger.debug("Operation details")
              logger.info("Operation completed successfully")
          except Exception as e:
              logger.error(f"Operation failed: {str(e)}")
              raise

3. Log levels available:
   - DEBUG: Detailed information for debugging
   - INFO: General operational information
   - WARNING: Warning messages for potential issues
   - ERROR: Error messages for failed operations
   - CRITICAL: Critical errors requiring immediate attention

4. Log file rotation:
   - Log files are automatically rotated when they reach 10MB
   - Up to 5 backup files are kept
   - Backup files are named with a timestamp suffix

5. Example usage in different contexts:

   a. In API endpoints:
   .. code-block:: python

      @router.post("/items")
      async def create_item(item: ItemCreate):
          logger.info(f"Creating new item: {item.name}")
          try:
              result = await item_service.create(item)
              logger.info(f"Item created successfully: {result.id}")
              return result
          except Exception as e:
              logger.error(f"Failed to create item: {str(e)}")
              raise HTTPException(status_code=500, detail=str(e))

   b. In background tasks:
   .. code-block:: python

      async def process_background_task():
          logger.info("Starting background task")
          try:
              # Process data
              logger.debug("Processing data chunk")
              # More processing
              logger.info("Background task completed")
          except Exception as e:
              logger.error(f"Background task failed: {str(e)}")
              raise

   c. In database operations:
   .. code-block:: python

      async def save_to_database(data: dict):
          logger.info("Saving data to database")
          try:
              async with db.transaction():
                  result = await db.execute(query, data)
                  logger.debug(f"Database operation result: {result}")
                  return result
          except Exception as e:
              logger.error(f"Database operation failed: {str(e)}")
              raise

Development Workflow
------------------

1. Create a new branch for your feature:
   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and commit them:
   .. code-block:: bash

      git add .
      git commit -m "feat: add new feature"

3. Push your changes:
   .. code-block:: bash

      git push origin feature/your-feature-name

4. Create a pull request

Code Style
---------

The project follows these code style guidelines:

* Follow PEP 8 guidelines
* Use type hints for all function parameters and return values
* Write docstrings for all public functions and classes
* Keep functions focused and small
* Use meaningful variable and function names
* Comment complex logic, not obvious code

Testing
-------

1. Write unit tests for all new features
2. Maintain test coverage above 80%
3. Use appropriate test markers (unit, integration, slow)
4. Run tests before committing:
   .. code-block:: bash

      pytest

Documentation
------------

1. Keep documentation up to date
2. Use clear and concise language
3. Include examples where appropriate
4. Document API endpoints with OpenAPI/Swagger
5. Build documentation locally:
   .. code-block:: bash

      cd docs
      make html

CI/CD
-----

The project includes GitHub Actions workflows for:

* Code quality checks
* Testing
* Documentation building
* Dependency updates
* Security scanning
* Release management

Security
--------

* Never commit sensitive information
* Use environment variables for secrets
* Regular security audits with Bandit
* Keep dependencies updated
* Follow security best practices

Next Steps
---------

1. Review the :doc:`development` guide for detailed development guidelines
2. Check out the :doc:`testing` guide for testing best practices
3. Read the :doc:`deployment` guide for deployment instructions
4. Explore the :doc:`../api/modules` for API documentation
5. Look at the :doc:`../examples/notebooks` for example usage 