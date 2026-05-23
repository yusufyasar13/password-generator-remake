
# Project Title

A brief description of what this project does and who it's for

# 🔐 Secure Password Generator & Vault

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)

The **Secure Password Generator & Vault** is a professional Python desktop application designed to generate cryptographically secure passwords and store them safely in a locally encrypted SQLite database. 

Upgraded from its legacy Tkinter version, this application now features a modern PyQt6 interface, MVC architecture, and bank-level AES (Fernet) encryption.
## Screenshots

![App Screenshot](https://github.com/yusufyasar13/password-generator-remake/blob/main/password_generator/screenshots/password_generator_ss_1.png)

![App Screenshot](https://github.com/yusufyasar13/password-generator-remake/blob/main/password_generator/screenshots/password_generator_ss_2.png)

## ✨ Features

- **Cryptographically Secure:** Uses Python's `secrets` module instead of `random` to ensure unpredictable, hacker-proof passwords.
- **Encrypted Local Vault:** Passwords are encrypted using AES (Fernet) cryptography and stored safely in a local SQLite database (`vault.db`).
- **Modern UI:** A clean, user-friendly, and responsive graphical interface built with PyQt6.
- **Customizable Passwords:** Choose length (8-32) and toggle letters, numbers, and special symbols.
- **Vault Manager:** A built-in dialog to view decrypted passwords and delete old records.
- **One-Click Copy:** Easily copy generated passwords to your clipboard with visual feedback.## 🚀 Option 1: Standalone Executable (Recommended for Regular Users)

There are two ways to use this application. If you just want to use the app without dealing with code:

1) Go to the **[Releases](https://github.com/yusufyasar13/password-generator-remake/releases)** section on the right side of this GitHub repository.
2) Download the latest `password_generator.exe` file.
3) Python installation is **not required**.
4) Simply double-click the `.exe` file to run the application.

*(Note: When you save your first password, the app will generate `secret.key` and `vault.db` files in the same folder. Keep them together with the `.exe` file!)*## 💻 Option 2: Run from Source (For Developers)

1) Clone or download this code repository to your computer and unzip the downloaded file:
```bash 
git clone [https://github.com/yusufyasar13/password-generator-remake.git](https://github.com/yusufyasar13/password-generator-remake)
```

2) Ensure you have Python 3.x installed on your system.

3) Open your terminal or command prompt, navigate to the project directory, and install the required libraries:
```bash 
pip install -r requirements.txt
```

4) Run the application using the following command:
```bash 
python main.py
```

```markdown
## ⚠️ Important Security Notice

When you save your first password, the application automatically creates a **`secret.key`** file. 
**DO NOT DELETE OR LOSE THIS FILE!** 
It is the master key to your vault. If this file is lost, the encrypted passwords inside `vault.db` cannot be recovered by anyone.## 📄 License

This application is open-source and distributed under the MIT License. For more information, refer to the [LICENSE](https://github.com/yusufyasar13/password-generator-remake/blob/main/LICENSE) file.
