Welcome to AI-Powered Project's documentation!
===========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   guides/getting_started
   guides/development
   guides/testing
   guides/deployment
   api/modules
   examples/notebooks

Features
--------

* Modern Python packaging with `pyproject.toml`
* Type checking with `mypy`
* Code formatting with `black` and `isort`
* Linting with `ruff`
* Testing with `pytest` and coverage reporting
* Pre-commit hooks for code quality
* FastAPI for API development
* OpenAI integration ready
* Environment variable management with `python-dotenv`
* Comprehensive documentation with Sphinx
* CI/CD templates for GitHub Actions
* Security scanning with Bandit
* Code coverage reporting
* Automated dependency updates

Quick Start
----------

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

For more detailed information, see the :doc:`guides/getting_started` guide.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 