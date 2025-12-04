# src/tools/validation.py
import re
from typing import Dict, Any

def validate_email(email: str) -> Dict[str, Any]:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, email))
    
    return {
        "is_valid_format": is_valid,
        "email": email
    }
