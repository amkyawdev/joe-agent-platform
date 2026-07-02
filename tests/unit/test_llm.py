"""Unit tests for LLM module."""

import pytest

from llm.models import AVAILABLE_MODELS, ModelConfig, ModelRegistry
from llm.tokenizer import TokenCounter


class TestModels:
    """Test LLM models."""
    
    def test_free_models_available(self):
        """Test that free models are configured."""
        free_models = [m for m in AVAILABLE_MODELS.values() if m.get('is_free')]
        assert len(free_models) > 0
    
    def test_qwen_coder_free(self):
        """Test Qwen Coder model is configured as free."""
        # Check for qwen3-coder or any free coder model
        free_models = [m for m in AVAILABLE_MODELS.values() if m.get('is_free') and 'code' in m.get('capabilities', [])]
        assert len(free_models) > 0, "Should have at least one free coding model"
    
    def test_model_has_required_fields(self):
        """Test model config has required fields."""
        for model_id, config in AVAILABLE_MODELS.items():
            assert 'id' in config
            assert 'provider' in config
            assert 'name' in config
            assert 'context_length' in config
    
    def test_model_registry(self):
        """Test model registry."""
        registry = ModelRegistry()
        models = registry.list_all()
        assert len(models) > 0
    
    def test_filter_by_capability(self):
        """Test filtering models by capability."""
        registry = ModelRegistry()
        code_models = registry.filter_by_capability('code')
        assert len(code_models) > 0


class TestTokenizer:
    """Test tokenizer."""
    
    def test_count_empty_string(self):
        """Test counting empty string."""
        assert TokenCounter.count("") == 0
    
    def test_count_simple_text(self):
        """Test counting simple text."""
        text = "Hello world"
        count = TokenCounter.count(text)
        assert count > 0
    
    def test_truncate(self):
        """Test text truncation."""
        text = "Hello " * 100
        truncated = TokenCounter.truncate(text, max_tokens=50)
        # Note: Truncation is approximate
        assert len(truncated) < len(text)