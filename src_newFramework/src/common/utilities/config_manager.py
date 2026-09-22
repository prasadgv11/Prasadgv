"""
Deprecated: kept only so existing imports keep working.
The real implementation now lives in config_loader.py.
"""
from src.common.utilities.config_loader import (
    ConfigManager,
    ConfigError,
    available_banks,
)

__all__ = ["ConfigManager", "ConfigError", "available_banks"]