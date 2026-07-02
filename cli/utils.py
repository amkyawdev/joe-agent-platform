"""CLI utilities for configuration and logging."""

import os
import sys
from pathlib import Path
from typing import Optional

import structlog
from dotenv import load_dotenv

from config.settings import Settings


def setup_logging(verbose: bool = False) -> None:
    """Configure structured logging."""
    log_level = "DEBUG" if verbose else "INFO"
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(colors=True)
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level)
    )


def load_config(config_path: Optional[str] = None) -> Settings:
    """Load configuration from environment or file."""
    env_file = Path(config_path) if config_path else Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
    else:
        load_dotenv()
    
    return Settings()