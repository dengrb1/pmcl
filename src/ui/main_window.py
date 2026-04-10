"""
Main window UI component for PMCL.
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from ..config import (
    ConfigManager,
    DEFAULT_USERNAME,
    DEFAULT_MAX_MEMORY_MB,
    GAME_VERSIONS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from ..core import GameLauncher
from ..utils.styles import Styles
from .settings_dialog import SettingsDialog
from .vape_select_dialog import VapeSelectDialog


class MainWindow(QtWidgets.QMainWindow):
    """Main application window."""

    def __init__(self, config_manager: ConfigManager = None):
        super().__init__()
        self.config_manager = config_manager or ConfigManager()
        self.game_launcher = GameLauncher()
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        """Initialize the UI components."""
        self.setObjectName("MainWindow")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Username input
        self._setup_username_input()

        # Title label
        self._setup_title_label()

        # Game version selector
        self._setup_game_version_selector()

        # Memory input
        self._setup_memory_input()

        # Buttons
        self._setup_buttons()

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.setCentralWidget(self.centralwidget)
        self.retranslate_ui()

    def _setup_username_input(self):
        """Setup username input field."""
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontalLayout_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        horizontal_layout.addWidget(self.label_3)

        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setObjectName("username")
        self.username.setStyleSheet(Styles.LINE_EDIT)
        horizontal_layout.addWidget(self.username)

        self.gridLayout.addLayout(horizontal_layout, 1, 2, 1, 3)

    def _setup_title_label(self):
        """Setup title label."""
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 4)

    def _setup_game_version_selector(self):
        """Setup game version combobox."""
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontalLayout")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        horizontal_layout.addWidget(self.label_2)

        self.game_c = QtWidgets.QComboBox(self.centralwidget)
        self.game_c.setObjectName("game_c")
        self.game_c.setStyleSheet(Styles.COMBO_BOX_DEFAULT)
        for version in GAME_VERSIONS:
            self.game_c.addItem(version)
        horizontal_layout.addWidget(self.game_c)

        self.gridLayout.addLayout(horizontal_layout, 2, 1, 1, 2)

    def _setup_memory_input(self):
        """Setup memory input field."""
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontalLayout_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        horizontal_layout.addWidget(self.label_4)

        self.maxmb_t = QtWidgets.QLineEdit(self.centralwidget)
        self.maxmb_t.setObjectName("maxmb_t")
        self.maxmb_t.setStyleSheet(Styles.LINE_EDIT)
        horizontal_layout.addWidget(self.maxmb_t)

        self.gridLayout.addLayout(horizontal_layout, 1, 1, 1, 1)

    def _setup_buttons(self):
        """Setup all buttons."""
        # Run game button
        self.run_game = QtWidgets.QPushButton(self.centralwidget)
        self.run_game.setObjectName("run_game")
        self.run_game.setStyleSheet(Styles.BUTTON_RUN_GAME)
        self.run_game.clicked.connect(self.run_game_handler)
        self.gridLayout.addWidget(self.run_game, 4, 1, 1, 1)

        # Load config button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(Styles.BUTTON_DARK)
        self.pushButton_2.clicked.connect(self.load_config)
        self.gridLayout.addWidget(self.pushButton_2, 2, 3, 1, 2)

        # Vape button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(Styles.BUTTON_PRIMARY)
        self.pushButton.clicked.connect(self.open_vape_dialog)
        self.gridLayout.addWidget(self.pushButton, 4, 3, 1, 1)

        # Settings button
        self.settings = QtWidgets.QPushButton(self.centralwidget)
        self.settings.setObjectName("settings")
        self.settings.setStyleSheet(Styles.BUTTON_SETTINGS)
        self.settings.clicked.connect(self.open_settings)
        self.gridLayout.addWidget(self.settings, 4, 4, 1, 1)

    def retranslate_ui(self):
        """Set UI text translations."""
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Python minecraft launcher V1.1"))
        self.label_3.setText(_translate("MainWindow", "游戏姓名："))
        self.label.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#1c33fe;">Python minecraft launcher V1.1</span></p></body></html>',
            )
        )
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:11pt;">游戏版本：</span></p></body></html>',
            )
        )
        self.pushButton.setText(_translate("MainWindow", "开 vape"))
        self.settings.setText(_translate("MainWindow", "设置"))
        self.label_4.setText(_translate("MainWindow", "最大内存："))
        self.run_game.setText(_translate("MainWindow", "开始游戏"))
        self.pushButton_2.setText(_translate("MainWindow", "读取配置"))

    def load_config(self):
        """Load configuration from storage and update UI."""
        config = self.config_manager.load_config()
        self.username.setText(config.get("username", DEFAULT_USERNAME))
        self.maxmb_t.setText(config.get("maxmb", str(DEFAULT_MAX_MEMORY_MB)))
        
        version = config.get("version", "")
        if version:
            self.game_c.setCurrentText(version)

    def save_config(self):
        """Save current UI values to configuration storage."""
        username = self.username.text()
        maxmb = self.maxmb_t.text()
        version = self.game_c.currentText()
        
        self.config_manager.save_config(username, maxmb, version)
        self.config_manager.save_text_files(username, maxmb, version)

    def run_game_handler(self):
        """Handle game launch button click."""
        username = self.username.text()
        maxmb = self.maxmb_t.text()
        version = self.game_c.currentText()

        # Validate parameters
        is_valid, error_msg = self.game_launcher.validate_launch_params(
            username, maxmb, version
        )
        
        if not is_valid:
            QMessageBox.critical(self, "Error", error_msg)
            return

        # Save configuration
        self.save_config()

        # Launch game
        success = self.game_launcher.launch_game()
        if not success:
            QMessageBox.critical(self, "Error", "启动失败！未知错误？")

    def open_vape_dialog(self):
        """Open vape selection dialog."""
        dialog = VapeSelectDialog(self)
        dialog.exec_()

    def open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self.config_manager, self)
        dialog.exec_()
