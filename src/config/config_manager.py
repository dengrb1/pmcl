"""
Configuration manager for the launcher.
Handles loading and saving user settings.
"""

import shelve
from pathlib import Path
from typing import Optional, Dict, Any

from .constants import (
    CONFIG_FILE,
    USERNAME_FILE,
    MAXMB_FILE,
    VERSION_FILE,
    DB_KEY_USERNAME,
    DB_KEY_MAXMB,
    DB_KEY_VERSION,
    DB_KEY_VAPER,
    DB_KEY_STARTGAME,
    DB_KEY_VAPE_V,
    DEFAULT_USERNAME,
    DEFAULT_MAX_MEMORY_MB,
)


class ConfigManager:
    """Manages application configuration storage and retrieval."""

    def __init__(self, config_dir: str = "."):
        self.config_dir = Path(config_dir)
        self._db_path = self.config_dir / CONFIG_FILE

    def _get_db(self) -> shelve.DbfilenameShelf:
        """Open database connection."""
        # Ensure directory exists
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        return shelve.open(str(self._db_path))

    def load_config(self) -> Dict[str, Any]:
        """Load all configuration values from database."""
        with self._get_db() as db:
            return {
                DB_KEY_USERNAME: db.get(DB_KEY_USERNAME, DEFAULT_USERNAME),
                DB_KEY_MAXMB: db.get(DB_KEY_MAXMB, str(DEFAULT_MAX_MEMORY_MB)),
                DB_KEY_VERSION: db.get(DB_KEY_VERSION, ""),
                DB_KEY_VAPER: db.get(DB_KEY_VAPER, False),
                DB_KEY_STARTGAME: db.get(DB_KEY_STARTGAME, False),
                DB_KEY_VAPE_V: db.get(DB_KEY_VAPE_V, ""),
            }

    def save_config(self, username: str, maxmb: str, version: str) -> None:
        """Save main configuration values to database."""
        with self._get_db() as db:
            db[DB_KEY_USERNAME] = username
            db[DB_KEY_MAXMB] = maxmb
            db[DB_KEY_VERSION] = version

    def save_text_files(self, username: str, maxmb: str, version: str) -> None:
        """Save configuration to text files (legacy support)."""
        (self.config_dir / USERNAME_FILE).write_text(username)
        (self.config_dir / MAXMB_FILE).write_text(maxmb)
        (self.config_dir / VERSION_FILE).write_text(version)

    def reset_vaper_status(self) -> None:
        """Reset vape launch status."""
        with self._get_db() as db:
            db[DB_KEY_VAPER] = False

    def reset_game_start_status(self) -> None:
        """Reset game launch status."""
        with self._get_db() as db:
            db[DB_KEY_STARTGAME] = False

    def delete_config(self) -> None:
        """Delete all configuration values."""
        with self._get_db() as db:
            db[DB_KEY_USERNAME] = ""
            db[DB_KEY_MAXMB] = ""
            db[DB_KEY_VERSION] = ""

    def set_vape_version(self, version: str) -> None:
        """Set vape version."""
        with self._get_db() as db:
            db[DB_KEY_VAPE_V] = version

    def get_vape_version(self) -> Optional[str]:
        """Get stored vape version."""
        with self._get_db() as db:
            return db.get(DB_KEY_VAPE_V)
