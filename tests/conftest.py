import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture that provides a TestClient instance"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Fixture that provides a deep copy of activities to isolate test state"""
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(fresh_activities):
    """Fixture that resets activities before each test"""
    # Store original activities
    original = deepcopy(app.activities)
    
    # Replace with fresh copy
    app.activities.clear()
    app.activities.update(fresh_activities)
    
    yield
    
    # Restore original activities after test
    app.activities.clear()
    app.activities.update(original)
