import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setup_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    log_file = os.path.join(log_dir, 'diary_app.log')
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Create handlers
    # Rotating file handler (10MB per file, keep 5 backup files)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    # Create logger
    logger = logging.getLogger('diary_app')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Create separate loggers for different components
    component_loggers = {
        'storage': logging.getLogger('diary_app.storage'),
        'ui': logging.getLogger('diary_app.ui'),
        'metadata': logging.getLogger('diary_app.metadata'),
        'export': logging.getLogger('diary_app.export')
    }

    # Configure component loggers
    for component_logger in component_loggers.values():
        component_logger.setLevel(logging.DEBUG)
        component_logger.addHandler(file_handler)
        component_logger.addHandler(console_handler)

    return logger, component_loggers

def get_logger(component=None):
    """Get a logger for a specific component or the main logger."""
    if component:
        return logging.getLogger(f'diary_app.{component}')
    return logging.getLogger('diary_app')

# Logging utility functions
def log_error(logger, error, context=None):
    """Log an error with context information."""
    message = f"Error: {str(error)}"
    if context:
        message = f"{message} (Context: {context})"
    logger.error(message, exc_info=True)

def log_operation(logger, operation, details=None):
    """Log an operation with optional details."""
    message = f"Operation: {operation}"
    if details:
        message = f"{message} - {details}"
    logger.info(message)

def log_metadata(logger, metadata_type, data):
    """Log metadata collection."""
    logger.debug(f"Collected {metadata_type}: {data}")

def log_performance(logger, operation, duration):
    """Log performance metrics."""
    logger.debug(f"Performance - {operation}: {duration:.2f} seconds") 