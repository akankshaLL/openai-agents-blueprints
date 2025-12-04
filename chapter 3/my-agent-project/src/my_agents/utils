# src/utils/logging.py
import logging
import sys
from typing import Optional

from src.config.settings import settings

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Set up a logger with the specified name and level."""
    logger = logging.getLogger(name)
    
    # Set log level from settings or parameter
    log_level = level or settings.log_level
    logger.setLevel(getattr(logging, log_level))
    
    # Create console handler if not already added
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Create a default application logger
app_logger = setup_logger("my_agent_app")
