"""
Pytest configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.dependencies import reset_dependencies, get_repositories, get_services


@pytest.fixture(scope="function")
def client():
    """
    Create a test client for each test.
    
    Resets dependencies to ensure clean state.
    """
    reset_dependencies()
    # Re-initialize dependencies with fresh data
    _ = get_repositories()
    _ = get_services()
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    reset_dependencies()


@pytest.fixture
def repositories():
    """Get initialized repositories."""
    reset_dependencies()
    return get_repositories()


@pytest.fixture
def services():
    """Get initialized services."""
    reset_dependencies()
    _ = get_repositories()  # Ensure repos are initialized first
    return get_services()
