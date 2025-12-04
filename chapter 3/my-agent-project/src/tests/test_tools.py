# tests/test_tools.py
import pytest
from unittest.mock import patch, MagicMock
from src.my_agents.specialized.customer_support import _get_product_info_impl

class TestProductTools:
    """Test suite for product-related tools."""
    
    def test_get_product_info_valid_id(self):
        """Test product info retrieval with valid product ID."""
        result = _get_product_info_impl("PROD123")
        
        assert isinstance(result, str)
        assert "PROD123" in result
        assert "sample product description" in result
    
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("invalid.email", False),
        ("user@", False),
        ("@example.com", False),
        ("user.name+tag@example.com", True),
    ])
    def test_validate_email(self, email, expected):
        """Test email validation with various inputs."""
        from src.tools.validation import validate_email
        result = validate_email(email)
        assert result["is_valid_format"] == expected
