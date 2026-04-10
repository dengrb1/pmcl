"""Configuration package for PMCL."""

from .constants import *
from .config_manager import ConfigManager

__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "WINDOW_WIDTH",
    "WINDOW_HEIGHT",
    "DEFAULT_USERNAME",
    "DEFAULT_MAX_MEMORY_MB",
    "MIN_MEMORY_MB",
    "CONFIG_FILE",
    "USERNAME_FILE",
    "MAXMB_FILE",
    "VERSION_FILE",
    "GAME_VERSIONS",
    "VAPE_VERSIONS",
    "DB_KEY_USERNAME",
    "DB_KEY_MAXMB",
    "DB_KEY_VERSION",
    "DB_KEY_VAPER",
    "DB_KEY_STARTGAME",
    "DB_KEY_VAPE_V",
    "ConfigManager",
]
