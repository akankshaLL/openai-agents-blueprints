# src/utils/tracing.py
from typing import Optional, Dict, Any
from agents import trace, set_tracing_disabled, set_trace_processors
from agents.tracing import add_trace_processor

from ..config.settings import settings
from .logging import setup_logger

logger = setup_logger(__name__)

def configure_tracing(
    workflow_name: Optional[str] = None,
    group_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
):
    """Configure tracing for the application."""
    if not settings.enable_tracing:
        logger.info("Tracing is disabled")
        set_tracing_disabled(True)
        return
    
    workflow = workflow_name or settings.trace_workflow_name
    logger.info(f"Configuring tracing for workflow: {workflow}")
    
    # You could add custom trace processors here
    # For example, to send traces to a monitoring system
    # add_trace_processor(your_custom_processor)
    
    return {
        "workflow_name": workflow,
        "group_id": group_id,
        "metadata": metadata or {},
    }
