"""
Stylesheet definitions for the application UI.
Centralizes all CSS-like styles to avoid duplication.
"""


class Styles:
    """Contains all stylesheet definitions used in the application."""

    # Input field styles
    LINE_EDIT = """
        QLineEdit {
            border-top: none;
            border-left: none;
            border-right: none;
            border-bottom: 1px solid black;
            background-color: transparent;
        }
        
        QLineEdit:focus {
            border-bottom: 1px solid #2a70f4;
        }
    """

    # ComboBox styles
    COMBO_BOX_DEFAULT = """
        QComboBox {
            background-color: white;
            color: black;
            border: 1px solid lightgray;
            border-radius: 15px;
            padding-left: 15px;
        }
        
        QComboBox:on {
            border: 1px solid #63acfb;
        }

        QComboBox::drop-down {
            width: 22px;
            border-left: 1px solid lightgray;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
        }
        
        QComboBox::drop-down:on {
            border-left: 1px solid #63acfb;
        }

        QComboBox::down-arrow {
            width: 16px;
            height: 16px;
            image: url(PATH_TO_IMG);
        }

        QComboBox::down-arrow:on {
            image: url(PATH_TO_IMG);
        }

        QComboBox QAbstractItemView {
            color: black;
            border: none;
            outline: none;
            background-color: whitesmoke;
        }

        QComboBox QScrollBar:vertical {
            width: 2px;
            background-color: white;
        }

        QComboBox QScrollBar::handle:vertical {
            background-color: #b2bdaf;
        }
    """

    COMBO_BOX_GRAY = """
        QComboBox {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:1, stop:0 #f5f5f7, stop:1 #dedee0);
            border: 1px solid whitesmoke;
            border-radius: 3px;
            padding-left: 15px;
            color: gray;
        }

        QComboBox::drop-down {
            width: 22px;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

        QComboBox::down-arrow {
            width: 16px;
            height: 16px;
            image: url(PATH_TO_IMG);
        }

        QComboBox QAbstractItemView {
            color: gray;
            border: none;
            outline: none;
            background-color: #dedee0;
        }

        QComboBox QScrollBar:vertical {
            width: 2px;
            background-color: white;
        }

        QComboBox QScrollBar::handle:vertical {
            background-color: #b2bdaf;
        }
    """

    # Button styles
    BUTTON_PRIMARY = """
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #47a7ed, stop: 1 #a967b2);
            color: white;
            font-size: 20px;
            font-weight: bold;
            border-radius: 25px;
        }
        
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #459ee0, stop: 1 #995da1);
        }
        
        QPushButton:pressed {
            background-color: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #4093d1, stop: 1 #87538e);
        }
    """

    BUTTON_SETTINGS = """
        QPushButton {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:0.3, stop:0 #8a9195, stop:1 black);
            color: white;
            font-size: 20px;
            font-weight: bold;
            border-radius: 25px;
        }

        QPushButton:hover {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:0.3, stop:0 #7d8488, stop:1 black);
        }

        QPushButton:pressed {
            background-color: qlineargradient(x1:1, y1:0, x2:1, y2:0.3, stop:0 #6a7073, stop:1 black);
        }
    """

    BUTTON_RUN_GAME = """
        QPushButton {
            background-color: #57bd6a;
            color: #f9ffff;
            font-size: 20px;
            font-weight: bold;
            border-radius: 5px;
        }

        QPushButton:pressed {
            background-color: #4eaa5f;
        }
    """

    BUTTON_DARK = """
        QPushButton {
            background-color: #292929;
            border-radius: 5px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            border: 1px solid white;
        }

        QPushButton:pressed {
            background-color: black;
        }
    """
