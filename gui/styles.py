
MODERN_STYLE = """
/* Global */
QWidget {
    font-family: "Segoe UI", "Microsoft YaHei UI", sans-serif;
    font-size: 14px;
    color: #333;
    background-color: #f5f6f7;
}

/* GroupBox */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-top: 1.2em;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #0078d4;
    font-weight: bold;
}

/* Buttons */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 5px 15px;
    color: #333;
}
QPushButton:hover {
    background-color: #eef6fc;
    border-color: #0078d4;
    color: #0078d4;
}
QPushButton:pressed {
    background-color: #cfe4fa;
}
QPushButton:disabled {
    background-color: #f0f0f0;
    border-color: #d0d0d0;
    color: #a0a0a0;
}

/* Primary Button (Start) */
QPushButton#primary {
    background-color: #0078d4;
    color: white;
    border: none;
    font-weight: bold;
}
QPushButton#primary:hover {
    background-color: #006abc;
}
QPushButton#primary:pressed {
    background-color: #005a9e;
}

/* Success Button (Unpack) */
QPushButton#success {
    background-color: #107c10;
    color: white;
    border: none;
    font-weight: bold;
}
QPushButton#success:hover {
    background-color: #0b5e0b;
}

/* Inputs */
QLineEdit, QSpinBox, QComboBox, QTextEdit {
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 4px;
    background-color: white;
    selection-background-color: #0078d4;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {
    border-color: #0078d4;
}

/* TabWidget */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    background: white;
    border-radius: 4px;
}
QTabBar::tab {
    background: #f0f0f0;
    border: 1px solid #e0e0e0;
    border-bottom-color: #e0e0e0; /* same as pane */
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 16px;
    margin-right: 2px;
    color: #666;
}
QTabBar::tab:selected, QTabBar::tab:hover {
    background: white;
    color: #0078d4;
    font-weight: bold;
    border-bottom-color: white; 
}

/* ProgressBar */
QProgressBar {
    border: none;
    background-color: #e0e0e0;
    border-radius: 4px;
    text-align: center;
    height: 10px;
}
QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 4px;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #cdcdcd;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
