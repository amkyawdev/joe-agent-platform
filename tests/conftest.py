"""Pytest configuration."""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "Hello, this is a test message for testing purposes."


@pytest.fixture
def sample_code():
    """Sample code for testing."""
    return """
def hello_world():
    print("Hello, World!")
    return True
"""


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "llm_model": "qwen3-coder-30b",
        "temperature": 0.7,
        "max_tokens": 4096
    }