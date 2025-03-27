"""
Logging configuration for the application.
"""
import logging
import logging.config
import logging.handlers
import os
from pathlib import Path
from typing import Optional, Dict, Any

from ..config import settings

def get_logging_config(
    log_level: str = "INFO",
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5,
    is_development: bool = False
) -> Dict[str, Any]:
    """
    Generate logging configuration dictionary.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format
        log_file: Path to log file
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        is_development: Whether to use development formatter
    
    Returns:
        Logging configuration dictionary
    """
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "dev": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "dev" if is_development else "default",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console"]
        }
    }
    
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "formatter": "default",  # Always use default formatter for file logs
            "filename": log_file,
            "maxBytes": max_bytes,
            "backupCount": backup_count
        }
        config["root"]["handlers"].append("file")
    
    return config

def setup_logging(
    log_level: str = "INFO",
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5,
    config_file: Optional[str] = None,
    is_development: Optional[bool] = None
) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format
        log_file: Path to log file
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        config_file: Path to logging configuration file
        is_development: Whether to use development formatter (defaults to APP_ENV == "development")
    """
    if config_file and os.path.exists(config_file):
        # Use configuration file if provided
        logging.config.fileConfig(config_file)
    else:
        # Use programmatic configuration
        if is_development is None:
            is_development = settings.APP_ENV == "development"
        
        config = get_logging_config(
            log_level=log_level,
            log_format=log_format,
            log_file=log_file,
            max_bytes=max_bytes,
            backup_count=backup_count,
            is_development=is_development
        )
        logging.config.dictConfig(config)
    
    # Log initial message
    logging.info("Logging configured successfully")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Configure logging on module import
setup_logging(
    log_level=settings.LOG_LEVEL,
    log_format=settings.LOG_FORMAT,
    log_file=settings.LOG_FILE
) 