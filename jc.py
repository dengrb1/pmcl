"""
Initialization module for PMCL.
Handles user consent and launches the main application.
"""

import sys
from time import sleep

from src.config import ConfigManager, DB_KEY_VAPER, DB_KEY_STARTGAME


def print_banner():
    """Print application banner."""
    print("版本:V1.1")
    print("正在初始化...")
    print(
        "可能会被 360 等杀毒软件杀掉，使用前请关闭杀毒软件或把此启动器的所有文件加入白名单！"
    )


def print_welcome():
    """Print welcome message."""
    print("欢迎使用 Python Minecraft Launcher！")
    print("项目地址:https://gitee.com/dengrb1/pmcl")
    print("作者:dengrb1")
    print("本项目完全没有病毒，您可以放心使用！!")


def initialize_config():
    """Initialize configuration database."""
    config_manager = ConfigManager()
    with config_manager._get_db() as db:
        db[DB_KEY_STARTGAME] = False
        db[DB_KEY_VAPER] = False


def run_main_app():
    """Launch the main application."""
    try:
        # Import here to avoid circular imports
        from PyQt5 import QtWidgets
        from src.ui import MainWindow
        
        app = QtWidgets.QApplication(sys.argv)
        config_manager = ConfigManager()
        window = MainWindow(config_manager=config_manager)
        window.show()
        sys.exit(app.exec_())
    except Exception:
        show_error()


def show_error():
    """Display error message and exit."""
    print("==================================")
    print("启动失败！")
    print("请检查文件是否完整再重启！")
    sleep(1)
    sys.exit()


def main():
    """Main entry point for jc.py functionality."""
    print_banner()
    
    ty = input("是否同意使用本软件（y/n）：")

    if ty.lower() == "y":
        print_welcome()
        initialize_config()
        print("初始化已完成！")
        sleep(1.2)
        run_main_app()
    elif ty.lower() == "n":
        print("已拒绝！")
        sleep(1)
        sys.exit()
    else:
        print("输入错误！")
        sleep(1)
        sys.exit()


if __name__ == "__main__":
    main()
