"""
Settings dialog UI component.
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from ..config import ConfigManager
from ..utils.styles import Styles


class SettingsDialog(QtWidgets.QDialog):
    """Settings dialog window."""

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components."""
        self.setObjectName("Form")
        self.resize(358, 300)
        self.setFixedSize(self.width(), self.height())

        # Layout widget
        self.layoutWidget = QtWidgets.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 50, 172, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Reset vape status button
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(Styles.BUTTON_SETTINGS)
        self.pushButton.clicked.connect(self.reset_vape_status)
        self.verticalLayout.addWidget(self.pushButton)

        # Reset game start status button
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(Styles.BUTTON_SETTINGS)
        self.pushButton_2.clicked.connect(self.reset_game_status)
        self.verticalLayout.addWidget(self.pushButton_2)

        # Delete config button
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet(Styles.BUTTON_PRIMARY)
        self.pushButton_5.clicked.connect(self.delete_config)
        self.verticalLayout.addWidget(self.pushButton_5)

        # Title label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(160, 10, 72, 31))
        self.label.setObjectName("label")

        self.retranslate_ui()

    def retranslate_ui(self):
        """Set UI text translations."""
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "设置"))
        self.pushButton.setText(_translate("Form", "重置 vape 启动状态"))
        self.pushButton_2.setText(_translate("Form", "重置游戏启动状态"))
        self.pushButton_5.setText(_translate("Form", "删除配置"))
        self.label.setText(
            _translate(
                "Form",
                '<html><head/><body><p><span style=" font-size:14pt; font-weight:600;">设置</span></p></body></html>',
            )
        )

    def reset_vape_status(self):
        """Reset vape launch status and close dialog."""
        self.config_manager.reset_vaper_status()
        QMessageBox.information(self, "提示", "处理成功！", QMessageBox.Ok)
        self.close()

    def reset_game_status(self):
        """Reset game launch status and close dialog."""
        self.config_manager.reset_game_start_status()
        QMessageBox.information(self, "提示", "处理成功！", QMessageBox.Ok)
        self.close()

    def delete_config(self):
        """Delete all configuration and close dialog."""
        self.config_manager.delete_config()
        QMessageBox.information(self, "提示", "处理成功!")
        self.close()
