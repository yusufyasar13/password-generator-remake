import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QCheckBox, QPushButton, QLineEdit, QSlider,
                             QDialog, QTableWidget, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

# ---- VAULT DIALOG (The Popup Window for Saved Passwords) ----
class VaultDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Vault")
        self.setFixedSize(400, 350)
        
        self.layout = QVBoxLayout(self)
        
        # Create a table to display passwords
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Platform", "Password"])
        
        # Stretch columns to fit the window perfectly
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        # Prevent users from editing the table cells directly
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # Select the whole row when clicked, not just a single cell
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.layout.addWidget(self.table)
        
        # Create the Delete button
        self.btn_delete = QPushButton("Delete Selected")
        self.btn_delete.setStyleSheet("background-color: #c0392b; color: white; padding: 8px; border-radius: 5px;")
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addWidget(self.btn_delete)

# ---- MAIN WINDOW ----
class PasswordView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Password Generator")
        self.setFixedSize(400, 600)
        
        # Find the correct path for icons (crucial for when the app is converted to .exe)
        try:
            self.base_path = sys._MEIPASS
        except Exception:
            self.base_path = os.path.abspath(".")
            
        # Set the main window icon (shown on the top-left and taskbar)
        key_icon_path = os.path.join(self.base_path, "icons", "key.ico")
        self.setWindowIcon(QIcon(key_icon_path))
        
        # Set up the central area where all widgets will be placed
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        # Call the function to draw all the buttons and sliders
        self._setup_ui()

    def _setup_ui(self):
        # 1. HEADER (Icon + Title)
        self.header_layout = QHBoxLayout()
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title_label = QLabel("Secure Password Generator")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        
        self.header_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.header_layout)

        # 2. PASSWORD LENGTH SLIDER
        self.length_layout = QHBoxLayout()
        self.length_label = QLabel("Length: 12")
        self.length_label.setStyleSheet("font-weight: bold;")
        
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(8)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(12)
        self.length_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        
        self.length_layout.addWidget(self.length_label)
        self.length_layout.addWidget(self.length_slider)
        self.main_layout.addLayout(self.length_layout)

        # 3. CHECKBOXES FOR CHARACTERS
        self.chk_letters = QCheckBox("Include Letters (a-z, A-Z)")
        self.chk_letters.setChecked(True)
        self.chk_digits = QCheckBox("Include Numbers (0-9)")
        self.chk_digits.setChecked(True)
        self.chk_symbols = QCheckBox("Include Symbols (!@#$%)")
        
        self.main_layout.addWidget(self.chk_letters)
        self.main_layout.addWidget(self.chk_digits)
        self.main_layout.addWidget(self.chk_symbols)

        # 4. GENERATE BUTTON
        self.btn_generate = QPushButton("Generate Password")
        self.btn_generate.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.btn_generate)

        # 5. RESULT DISPLAY BOX
        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("Generated password will appear here...")
        self.result_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #bdc3c7; border-radius: 5px;")
        self.result_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.result_input)

        # 6. COPY BUTTON
        self.btn_copy = QPushButton("Copy to Clipboard")
        self.btn_copy.setStyleSheet("background-color: #2980b9; color: white; padding: 8px; border-radius: 5px;")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.btn_copy)

        # 7. SAVE TO VAULT AREA
        self.save_layout = QHBoxLayout()
        self.platform_input = QLineEdit()
        self.platform_input.setPlaceholderText("Platform name? (e.g., GitHub)")
        self.platform_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px;")
        
        self.btn_save = QPushButton("Save to Vault")
        self.btn_save.setStyleSheet("background-color: #8e44ad; color: white; font-weight: bold; padding: 8px; border-radius: 5px;")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.save_layout.addWidget(self.platform_input)
        self.save_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(self.save_layout)
        
        # 8. VIEW VAULT BUTTON
        self.btn_view_vault = QPushButton("View Vault")
        self.btn_view_vault.setStyleSheet("background-color: #34495e; color: white; font-weight: bold; padding: 12px; border-radius: 5px; margin-top: 15px;")
        self.btn_view_vault.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_layout.addWidget(self.btn_view_vault)