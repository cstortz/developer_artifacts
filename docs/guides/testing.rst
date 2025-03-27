Testing Guide
============

This guide provides comprehensive information about testing practices, tools, and best practices for the project.

Test Organization
---------------

Project Structure
~~~~~~~~~~~~~~~

The test directory follows a structure that mirrors the source code:

.. code-block:: text

   tests/
   ├── __init__.py
   ├── conftest.py           # Test configuration and fixtures
   ├── unit/                 # Unit tests
   │   ├── __init__.py
   │   ├── test_core.py
   │   ├── test_models.py
   │   └── test_services.py
   ├── integration/          # Integration tests
   │   ├── __init__.py
   │   ├── test_api.py
   │   └── test_ai.py
   └── e2e/                  # End-to-end tests
       ├── __init__.py
       └── test_workflows.py

Test Categories
~~~~~~~~~~~~~

* Unit Tests: Test individual components in isolation
* Integration Tests: Test component interactions
* End-to-End Tests: Test complete workflows
* Performance Tests: Test system performance
* Security Tests: Test security features

Test Configuration
----------------

Fixtures
~~~~~~~

.. code-block:: python

   import pytest
   from typing import AsyncGenerator
   from fastapi.testclient import TestClient
   from sqlalchemy.ext.asyncio import AsyncSession

   @pytest.fixture
   async def db_session() -> AsyncGenerator[AsyncSession, None]:
       """Create a database session for testing."""
       async with AsyncSession(engine) as session:
           yield session
           await session.rollback()

   @pytest.fixture
   def test_client() -> Generator[TestClient, None, None]:
       """Create a test client for the API."""
       with TestClient(app) as client:
           yield client

   @pytest.fixture
   def mock_ai_service():
       """Create a mock AI service."""
       with patch("src.services.ai.OpenAIService") as mock:
           yield mock

Test Markers
~~~~~~~~~~

.. code-block:: python

   # pytest.ini
   [pytest]
   markers =
       unit: Unit tests
       integration: Integration tests
       e2e: End-to-end tests
       slow: Slow running tests
       security: Security tests
       performance: Performance tests

Unit Testing
-----------

Basic Unit Tests
~~~~~~~~~~~~~

.. code-block:: python

   def test_process_data():
       """Test data processing function."""
       input_data = [1, 2, 3]
       expected = [2, 4, 6]
       result = process_data(input_data)
       assert result == expected

   def test_validate_input():
       """Test input validation."""
       with pytest.raises(ValueError):
           validate_input("")

   @pytest.mark.parametrize("input,expected", [
       (1, 1),
       (2, 4),
       (3, 9),
   ])
   def test_square(input: int, expected: int):
       """Test square function with multiple inputs."""
       assert square(input) == expected

Async Unit Tests
~~~~~~~~~~~~~

.. code-block:: python

   @pytest.mark.asyncio
   async def test_async_function():
       """Test async function."""
       result = await async_function()
       assert result == expected

   @pytest.mark.asyncio
   async def test_async_context():
       """Test async context manager."""
       async with AsyncContext() as context:
           result = await context.do_something()
           assert result == expected

Mocking
~~~~~~

.. code-block:: python

   from unittest.mock import Mock, patch, AsyncMock

   def test_with_mock():
       """Test with mocked dependencies."""
       mock_service = Mock()
       mock_service.process.return_value = "mocked result"
       
       result = function_under_test(mock_service)
       assert result == "mocked result"
       mock_service.process.assert_called_once()

   @pytest.mark.asyncio
   async def test_with_async_mock():
       """Test with async mocked dependencies."""
       mock_service = AsyncMock()
       mock_service.process.return_value = "mocked result"
       
       result = await async_function_under_test(mock_service)
       assert result == "mocked result"
       mock_service.process.assert_called_once()

Integration Testing
----------------

API Testing
~~~~~~~~~

.. code-block:: python

   @pytest.mark.integration
   async def test_api_endpoint(test_client):
       """Test API endpoint."""
       response = await test_client.post(
           "/api/v1/generate",
           json={"prompt": "test prompt"}
       )
       assert response.status_code == 200
       assert "response" in response.json()

   @pytest.mark.integration
   async def test_api_error_handling(test_client):
       """Test API error handling."""
       response = await test_client.post(
           "/api/v1/generate",
           json={"prompt": ""}
       )
       assert response.status_code == 422

Database Testing
~~~~~~~~~~~~~

.. code-block:: python

   @pytest.mark.integration
   async def test_database_operations(db_session):
       """Test database operations."""
       # Create test data
       test_item = TestModel(name="test")
       db_session.add(test_item)
       await db_session.commit()
       
       # Query and verify
       result = await db_session.query(TestModel).first()
       assert result.name == "test"

   @pytest.mark.integration
   async def test_database_rollback(db_session):
       """Test database rollback."""
       # Create test data
       test_item = TestModel(name="test")
       db_session.add(test_item)
       await db_session.commit()
       
       # Verify data exists
       result = await db_session.query(TestModel).first()
       assert result is not None
       
       # Rollback should happen automatically after test

End-to-End Testing
----------------

Workflow Testing
~~~~~~~~~~~~~

.. code-block:: python

   @pytest.mark.e2e
   async def test_complete_workflow():
       """Test complete workflow."""
       # Initialize components
       client = TestClient(app)
       db = await setup_test_database()
       
       # Execute workflow
       response = await client.post(
           "/api/v1/workflow",
           json={"input": "test input"}
       )
       
       # Verify results
       assert response.status_code == 200
       result = response.json()
       assert result["status"] == "success"
       
       # Verify database state
       db_result = await db.query(WorkflowResult).first()
       assert db_result.status == "completed"

Performance Testing
----------------

Load Testing
~~~~~~~~~

.. code-block:: python

   @pytest.mark.performance
   async def test_api_performance():
       """Test API performance under load."""
       client = TestClient(app)
       start_time = time.time()
       
       # Send multiple concurrent requests
       tasks = [
           client.post("/api/v1/generate", json={"prompt": "test"})
           for _ in range(100)
       ]
       responses = await asyncio.gather(*tasks)
       
       end_time = time.time()
       duration = end_time - start_time
       
       # Verify performance metrics
       assert duration < 5.0  # Should complete within 5 seconds
       assert all(r.status_code == 200 for r in responses)

Security Testing
--------------

Input Validation
~~~~~~~~~~~~~

.. code-block:: python

   @pytest.mark.security
   def test_sql_injection_prevention():
       """Test SQL injection prevention."""
       malicious_input = "'; DROP TABLE users; --"
       with pytest.raises(ValidationError):
           validate_input(malicious_input)

   @pytest.mark.security
   def test_xss_prevention():
       """Test XSS prevention."""
       malicious_input = "<script>alert('xss')</script>"
       result = sanitize_input(malicious_input)
       assert "<script>" not in result

Coverage Requirements
------------------

Configuration
~~~~~~~~~~~

.. code-block:: python

   # .coveragerc
   [run]
   source = src
   omit =
       */tests/*
       */migrations/*
       */__init__.py

   [report]
   exclude_lines =
       pragma: no cover
       def __repr__
       raise NotImplementedError
       if __name__ == .__main__.:
       pass
       raise ImportError

   [html]
   directory = coverage_html

Running Tests
-----------

Basic Test Execution
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test categories
   pytest -m unit
   pytest -m integration
   pytest -m e2e

   # Run with coverage
   pytest --cov=src --cov-report=term-missing

   # Run specific test file
   pytest tests/unit/test_core.py

   # Run tests in parallel
   pytest -n auto

Debugging Tests
~~~~~~~~~~~~

.. code-block:: python

   def test_with_debugging():
       """Test with debugging capabilities."""
       import pdb; pdb.set_trace()  # Breakpoint
       result = function_under_test()
       assert result == expected

   # Run with verbose output
   pytest -v

   # Run with print statements
   pytest -s

Next Steps
---------

1. Review the :doc:`development` guide for development practices
2. Check out the :doc:`deployment` guide for deployment instructions
3. Explore the :doc:`../api/modules` for API documentation 