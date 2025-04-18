"""Configuration des tests."""
import pytest
from tests.mocks import MockVectorStore

@pytest.fixture(autouse=True)
def mock_vector_store(monkeypatch):
    """Mock du VectorStore pour tous les tests."""
    monkeypatch.setattr('src.orchestration.core.VectorStore', MockVectorStore) 