from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
from gui.view import VaultDialog

class PasswordController:
    # The brain of the application. It takes the View, Generator, and Vault and connects them together.
    def __init__(self, view, generator, vault):
        self.view = view
        self.generator = generator
        self.vault = vault
        
        # Automatically connect all buttons to their functions when the program starts
        self._connect_signals()

    def _connect_signals(self):
        # Connect the slider movement to the label text update
        self.view.length_slider.valueChanged.connect(self.update_length_label)
        
        # Connect buttons to their respective actions
        self.view.btn_generate.clicked.connect(self.generate_password)
        self.view.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.view.btn_save.clicked.connect(self.save_to_vault)
        self.view.btn_view_vault.clicked.connect(self.show_vault)

    def update_length_label(self, value):
        # Changes the text from "Length: 12" to whatever the slider value is
        self.view.length_label.setText(f"Length: {value}")

    def generate_password(self):
        # 1. Read what the user selected from the UI
        length = self.view.length_slider.value()
        use_letters = self.view.chk_letters.isChecked()
        use_digits = self.view.chk_digits.isChecked()
        use_symbols = self.view.chk_symbols.isChecked()
        
        try:
            # 2. Ask the generator to create a password based on these rules
            password = self.generator.generate(length, use_letters, use_digits, use_symbols)
            # 3. Show the generated password on the screen
            self.view.result_input.setText(password)
            # Reset the copy button text just in case it says "Copied!"
            self.view.btn_copy.setText("Copy to Clipboard")
        except ValueError as e:
            # If the user selected no checkboxes, show the error message
            self.view.result_input.setText("Error: " + str(e))

    def copy_to_clipboard(self):
        # Get the text currently inside the result box
        password = self.view.result_input.text()
        
        # If there is a real password (not empty and not an error), copy it to the computer's clipboard
        if password and not password.startswith("Error"):
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            # Give visual feedback to the user
            self.view.btn_copy.setText("Copied! ✓")

    def save_to_vault(self):
        password = self.view.result_input.text()
        # Remove extra spaces from the beginning and end of the platform name
        platform = self.view.platform_input.text().strip()

        # Validation 1: Prevent saving empty or error texts
        if not password or password.startswith("Error"):
            QMessageBox.warning(self.view, "Warning", "Please generate a valid password first!")
            return
            
        # Validation 2: Ensure the user typed a platform name
        if not platform:
            QMessageBox.warning(self.view, "Warning", "Please enter a platform name (e.g., GitHub)!")
            return

        # Send the data to the vault to be encrypted and saved
        self.vault.save_password(platform, password)
        
        # Inform the user and clear the input box for the next entry
        QMessageBox.information(self.view, "Success", f"Password for '{platform}' has been encrypted and saved!")
        self.view.platform_input.clear()

    def show_vault(self):
        # Create and show the popup window for the vault
        self.vault_dialog = VaultDialog(self.view)
        self.load_vault_data() 
        
        # Tell the delete button what to do when clicked
        self.vault_dialog.btn_delete.clicked.connect(self.delete_selected_password)
        
        self.vault_dialog.exec()

    def load_vault_data(self):
        # Clear the table first to avoid duplicate data
        self.vault_dialog.table.setRowCount(0)
        
        # Ask the vault for all decrypted passwords
        passwords = self.vault.get_all_passwords()
        
        # Loop through each password and place it in the correct row and column
        for row_idx, (row_id, platform, password) in enumerate(passwords):
            self.vault_dialog.table.insertRow(row_idx)
            
            item_platform = QTableWidgetItem(platform)
            # Secretly hide the database ID inside the platform item. We will need this if the user wants to delete it!
            item_platform.setData(Qt.ItemDataRole.UserRole, row_id) 
            
            item_password = QTableWidgetItem(password)
            
            # Place the items into the table (Row, Column)
            self.vault_dialog.table.setItem(row_idx, 0, item_platform)
            self.vault_dialog.table.setItem(row_idx, 1, item_password)

    def delete_selected_password(self):
        # Find out which row the user highlighted
        selected_items = self.vault_dialog.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.vault_dialog, "Warning", "Please select a record to delete.")
            return
            
        # Extract the hidden database ID from the selected row
        row = selected_items[0].row()
        item_platform = self.vault_dialog.table.item(row, 0)
        row_id = item_platform.data(Qt.ItemDataRole.UserRole)
        
        # Ask for confirmation before permanent deletion
        reply = QMessageBox.question(self.vault_dialog, 'Confirm', 'Are you sure you want to permanently delete this password?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.vault.delete_password(row_id)
            # Refresh the table so the deleted item disappears
            self.load_vault_data()