"""
Advanced Logging System for Hassan Ultimate Anti-Recoil
Comprehensive logging with performance monitoring and security features
"""

import logging
import logging.handlers
import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime


class PerformanceFilter(logging.Filter):
    """Filter for performance-related log messages."""
    
    def filter(self, record):
        return hasattr(record, 'performance') and record.performance


class SecurityFilter(logging.Filter):
    """Filter for security-related log messages."""
    
    def filter(self, record):
        return hasattr(record, 'security') and record.security


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for better readability."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'performance'):
            log_entry['performance'] = record.performance
        if hasattr(record, 'security'):
            log_entry['security'] = record.security
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        
        return json.dumps(log_entry)


class AsyncFileHandler(logging.handlers.RotatingFileHandler):
    """Asynchronous file handler for high-performance logging."""
    
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False):
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)
        self.buffer = []
        self.buffer_size = 100
        self.last_flush = time.time()
        
    def emit(self, record):
        try:
            msg = self.format(record)
            self.buffer.append(msg + '\n')
            
            # Flush buffer if full or timeout
            if len(self.buffer) >= self.buffer_size or time.time() - self.last_flush > 5.0:
                self._flush_buffer()
                
        except Exception:
            self.handleError(record)
    
    def _flush_buffer(self):
        """Flush the internal buffer to file."""
        if self.buffer:
            try:
                with open(self.baseFilename, 'a', encoding=self.encoding) as f:
                    f.writelines(self.buffer)
                self.buffer.clear()
                self.last_flush = time.time()
            except Exception:
                pass


def setup_logging(
    level: str = "INFO",
    log_dir: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True,
    enable_json: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Setup comprehensive logging system.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: logs/)
        enable_console: Enable console logging
        enable_file: Enable file logging
        enable_json: Enable JSON structured logging
        max_file_size: Maximum size of log files before rotation
        backup_count: Number of backup files to keep
    """
    
    # Create log directory
    if log_dir is None:
        log_dir = Path("logs")
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(exist_ok=True)
    
    # Get numeric level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(numeric_level)
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        
        # Use colored formatter for console
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # File handler for general logs
    if enable_file:
        log_file = log_dir / "hassan_antirecoil.log"
        file_handler = AsyncFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(numeric_level)
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # JSON structured logging
    if enable_json:
        json_file = log_dir / "hassan_antirecoil.json"
        json_handler = AsyncFileHandler(
            json_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        json_handler.setLevel(numeric_level)
        json_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(json_handler)
    
    # Performance logging
    perf_file = log_dir / "performance.log"
    perf_handler = AsyncFileHandler(
        perf_file,
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding='utf-8'
    )
    perf_handler.setLevel(logging.DEBUG)
    perf_handler.addFilter(PerformanceFilter())
    
    perf_formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S.%f'
    )
    perf_handler.setFormatter(perf_formatter)
    root_logger.addHandler(perf_handler)
    
    # Security logging
    security_file = log_dir / "security.log"
    security_handler = AsyncFileHandler(
        security_file,
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding='utf-8'
    )
    security_handler.setLevel(logging.WARNING)
    security_handler.addFilter(SecurityFilter())
    
    security_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    security_handler.setFormatter(security_formatter)
    root_logger.addHandler(security_handler)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("Hassan Ultimate Anti-Recoil v7.0 - Logging System Initialized")
    logger.info(f"Log Level: {level}")
    logger.info(f"Log Directory: {log_dir.absolute()}")


def get_performance_logger() -> logging.Logger:
    """Get logger for performance metrics."""
    logger = logging.getLogger('performance')
    return logger


def get_security_logger() -> logging.Logger:
    """Get logger for security events."""
    logger = logging.getLogger('security')
    return logger


def log_performance(message: str, **kwargs) -> None:
    """Log performance metric."""
    logger = get_performance_logger()
    extra = {'performance': True}
    extra.update(kwargs)
    logger.debug(message, extra=extra)


def log_security(message: str, level: str = "WARNING", **kwargs) -> None:
    """Log security event."""
    logger = get_security_logger()
    extra = {'security': True}
    extra.update(kwargs)
    
    numeric_level = getattr(logging, level.upper(), logging.WARNING)
    logger.log(numeric_level, message, extra=extra)


class ContextualLogger:
    """Logger with contextual information."""
    
    def __init__(self, name: str, context: Dict[str, Any] = None):
        self.logger = logging.getLogger(name)
        self.context = context or {}
    
    def _log(self, level: int, message: str, **kwargs):
        """Log with context."""
        extra = self.context.copy()
        extra.update(kwargs)
        self.logger.log(level, message, extra=extra)
    
    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log(logging.CRITICAL, message, **kwargs)
    
    def performance(self, message: str, **kwargs):
        """Log performance metric with context."""
        extra = self.context.copy()
        extra.update(kwargs)
        extra['performance'] = True
        self.logger.debug(message, extra=extra)
    
    def security(self, message: str, level: str = "WARNING", **kwargs):
        """Log security event with context."""
        extra = self.context.copy()
        extra.update(kwargs)
        extra['security'] = True
        numeric_level = getattr(logging, level.upper(), logging.WARNING)
        self.logger.log(numeric_level, message, extra=extra)


def get_contextual_logger(name: str, **context) -> ContextualLogger:
    """Get a logger with contextual information."""
    return ContextualLogger(name, context)


class LogManager:
    """Central log management system."""
    
    def __init__(self):
        self.loggers: Dict[str, ContextualLogger] = {}
        self.session_id = f"session_{int(time.time())}"
    
    def get_logger(self, name: str, **context) -> ContextualLogger:
        """Get or create a contextual logger."""
        if name not in self.loggers:
            full_context = {'session_id': self.session_id}
            full_context.update(context)
            self.loggers[name] = ContextualLogger(name, full_context)
        return self.loggers[name]
    
    def set_session_context(self, **context):
        """Set session-wide context for all loggers."""
        for logger in self.loggers.values():
            logger.context.update(context)
    
    def flush_all(self):
        """Flush all log handlers."""
        for handler in logging.getLogger().handlers:
            if hasattr(handler, '_flush_buffer'):
                handler._flush_buffer()
            else:
                handler.flush()


# Global log manager instance
log_manager = LogManager()