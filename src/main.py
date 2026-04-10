"""
PMCL - Python Minecraft Launcher

A simple Minecraft launcher with GUI.
"""

import sys
from PyQt5 import QtWidgets

from src.config import ConfigManager
from src.ui import MainWindow


def main():
    """Main entry point for the application."""
    app = QtWidgets.QApplication(sys.argv)
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create and show main window
    window = MainWindow(config_manager=config_manager)
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
