"""
Vape selection dialog UI component.
"""

import os
import subprocess
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from ..config import VAPE_VERSIONS
from ..utils.styles import Styles


class VapeSelectDialog(QtWidgets.QDialog):
    """Dialog for selecting vape version."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.work_dir = Path(".")
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components."""
        self.setObjectName("Form")
        self.resize(306, 250)
        self.setFixedSize(self.width(), self.height())

        # Confirm button
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(90, 190, 121, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(Styles.BUTTON_SETTINGS)
        self.pushButton.clicked.connect(self.launch_vape)
        
        # Title label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 20, 171, 31))
        self.label.setObjectName("label")
        
        # Version label
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(70, 100, 51, 21))
        self.label_2.setObjectName("label_2")
        
        # Version combobox
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(120, 100, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet(Styles.COMBO_BOX_GRAY)
        for version in VAPE_VERSIONS:
            self.comboBox.addItem(version)

        self.retranslate_ui()

    def retranslate_ui(self):
        """Set UI text translations."""
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "选择外挂"))
        self.pushButton.setText(_translate("Form", "确定"))
        self.label.setText(
            _translate(
                "Form",
                '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#ff0000;">请选择外挂</span></p></body></html>',
            )
        )
        self.label_2.setText(
            _translate(
                "Form",
                '<html><head/><body><p><span style=" font-size:11pt;">版本:</span></p></body></html>',
            )
        )

    def launch_vape(self):
        """Handle vape launch based on selected version."""
        selected_version = self.comboBox.currentText()

        if selected_version == "Vape lite":
            QMessageBox.information(
                self,
                "提示",
                "外挂获取渠道非官方渠道，请小心使用！",
                QMessageBox.Ok,
            )
            success = self._launch_vape_lite()
            if not success:
                QMessageBox.critical(
                    self, "ERROR", "启动失败！请检查文件！", QMessageBox.Ok
                )
        elif selected_version == "Vape V4":
            QMessageBox.critical(self, "ERROR", "无法使用！", QMessageBox.Ok)

        self.close()

    def _launch_vape_lite(self) -> bool:
        """Launch Vape Lite patcher."""
        try:
            fix_script = self.work_dir / "fix.bat"
            patcher_exe = self.work_dir / "Kangaroo Patcher.exe"

            if not fix_script.exists():
                raise FileNotFoundError("fix.bat not found")

            if not patcher_exe.exists():
                raise FileNotFoundError("Kangaroo Patcher.exe not found")

            # Run fix.bat first
            subprocess.run(str(fix_script), cwd=str(self.work_dir), shell=True)

            # Run patcher
            subprocess.Popen(
                f'"{patcher_exe}" Vape_Lite.exe',
                cwd=str(self.work_dir),
                shell=True,
            )
            return True
        except Exception:
            return False
