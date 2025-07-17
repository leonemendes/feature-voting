# Feature Voting System - Test Suite

Comprehensive test suite for the Feature Voting System Flask backend using pytest.

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Test configuration and fixtures
├── README.md                      # This file
├── unit/
│   ├── test_models.py            # Unit tests for database models
│   └── test_api.py               # Unit tests for API endpoints
└── integration/
    └── test_full_workflow.py     # Integration tests for complete workflows
```

## Test Categories

### Unit Tests
- **Model Tests**: Test Feature and Vote models independently
- **API Tests**: Test individual API endpoints and their responses
- **Error Handling**: Test error conditions and edge cases

### Integration Tests
- **Full Workflow**: Test complete feature lifecycle (create, vote, delete)
- **Concurrent Operations**: Test concurrent voting and feature creation
- **Data Consistency**: Test data integrity across operations

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run slow tests
pytest -m slow
```

### Run Specific Test Files
```bash
# Run model tests
pytest tests/unit/test_models.py

# Run API tests
pytest tests/unit/test_api.py

# Run integration tests
pytest tests/integration/test_full_workflow.py
```

### Run Specific Test Classes or Functions
```bash
# Run specific test class
pytest tests/unit/test_models.py::TestFeatureModel

# Run specific test function
pytest tests/unit/test_api.py::TestFeatureAPI::test_create_feature_success
```

### Test Coverage
Generate test coverage report:
```bash
pytest --cov=. --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## Test Configuration

### pytest.ini
The `pytest.ini` file configures:
- Test discovery patterns
- Coverage reporting
- Output formatting
- Test markers

### Fixtures
Common test fixtures in `conftest.py`:
- `app`: Flask application instance for testing
- `client`: Test client for making HTTP requests
- `db_connection`: Database connection for direct queries
- `sample_features`: Pre-created features for testing
- `sample_votes`: Pre-created votes for testing
- `sample_feature_data`: Sample data for feature creation tests
- `sample_vote_data`: Sample data for voting tests
- `test_helper`: Helper methods for common operations

## Test Data

### Sample Features
Tests use sample features with various characteristics:
- Features with different vote counts
- Features with and without descriptions
- Features for testing edge cases

### Sample Votes
Tests use sample votes to verify:
- Vote counting accuracy
- User vote tracking
- Duplicate vote prevention

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Test Markers
Use markers to categorize tests:
```python
@pytest.mark.unit
def test_feature_creation():
    # Unit test code

@pytest.mark.integration
def test_full_workflow():
    # Integration test code

@pytest.mark.slow
def test_performance():
    # Slow test code
```

### Using Fixtures
```python
def test_create_feature(client, sample_feature_data):
    # Use client fixture for HTTP requests
    # Use sample_feature_data fixture for test data
    response = client.post('/api/features', json=sample_feature_data['valid_feature'])
    assert response.status_code == 201
```

### Testing Database Operations
```python
def test_database_state(db_connection):
    # Use db_connection fixture for direct database queries
    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM features')
    count = cursor.fetchone()[0]
    assert count > 0
```

## Test Best Practices

### 1. Test Isolation
- Each test should be independent
- Use fixtures to provide clean test data
- Don't rely on test execution order

### 2. Clear Test Names
- Use descriptive test names that explain what is being tested
- Include expected behavior in the test name

### 3. Arrange, Act, Assert
- **Arrange**: Set up test data and conditions
- **Act**: Execute the code being tested
- **Assert**: Verify the expected outcomes

### 4. Test Edge Cases
- Test boundary conditions
- Test error conditions
- Test invalid inputs

### 5. Use Appropriate Assertions
```python
# Good: Specific assertions
assert response.status_code == 201
assert 'id' in response.get_json()

# Bad: Generic assertions
assert response.status_code != 500
assert response.get_json() is not None
```

## Continuous Integration

The test suite is designed to work with CI/CD systems:

```bash
# Run tests with coverage and output in CI format
pytest --cov=. --cov-report=xml --junit-xml=test-results.xml
```

## Debugging Tests

### Verbose Output
```bash
pytest -v
```

### Stop on First Failure
```bash
pytest -x
```

### Debug with pdb
```bash
pytest --pdb
```

### Run Specific Test with Output
```bash
pytest -s tests/unit/test_models.py::TestFeatureModel::test_feature_creation
```

## Common Issues

### Database Cleanup
If tests fail due to database state, ensure:
- Fixtures properly clean up after themselves
- Test isolation is maintained
- Database connections are closed

### Import Errors
If imports fail:
- Check PYTHONPATH includes the project root
- Verify all required dependencies are installed
- Check for circular imports

### Fixture Scope
If fixtures behave unexpectedly:
- Check fixture scope (function, class, module, session)
- Ensure fixtures are properly torn down
- Verify fixture dependencies

## Performance Considerations

### Test Speed
- Use `@pytest.mark.slow` for slow tests
- Consider using test doubles for external dependencies
- Use appropriate fixture scopes

### Database Performance
- Use in-memory databases for faster tests
- Minimize database operations in tests
- Use transactions for test isolation

## Extending the Test Suite

When adding new features:
1. Add unit tests for new models/functions
2. Add API tests for new endpoints
3. Add integration tests for new workflows
4. Update fixtures if needed
5. Update this README with new test categories