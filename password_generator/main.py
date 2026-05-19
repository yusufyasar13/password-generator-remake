import sys
from PyQt6.QtWidgets import QApplication

# Import all the separate pieces we built
from gui.view import PasswordView
from core.generator import PasswordGenerator
from core.database import PasswordVault
from controller import PasswordController

if __name__ == "__main__":
    # Start the underlying application process
    app = QApplication(sys.argv)
    
    # 1. Create the building blocks
    view = PasswordView()
    generator = PasswordGenerator()
    vault = PasswordVault()
    
    # 2. Hand all the blocks to the Controller so it can wire them together
    controller = PasswordController(view, generator, vault)
    
    # 3. Display the main window to the user
    view.show()
    
    # 4. Keep the application running until the user closes the window
    sys.exit(app.exec())