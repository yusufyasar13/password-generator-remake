import sqlite3
import os
from cryptography.fernet import Fernet

class PasswordVault:
    def __init__(self, db_name="vault.db", key_file="secret.key"):
        # We set the file names for our database and our secret encryption key.
        self.db_name = db_name
        self.key_file = key_file
        
        # We load the existing key or create a new one if it doesn't exist.
        self.key = self._load_or_create_key()
        
        # We create a 'cipher' (a locking mechanism) using our secret key.
        self.cipher = Fernet(self.key)
        
        # We prepare the database table when the program starts.
        self._init_db()

    def _load_or_create_key(self):
        # Check if the secret key file already exists in the folder
        if not os.path.exists(self.key_file):
            # If not, generate a brand new master key
            key = Fernet.generate_key()
            # Create the file and save the key inside it
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key
        else:
            # If the file exists, just open it and read the master key
            with open(self.key_file, "rb") as f:
                return f.read()

    def _init_db(self):
        # Connect to the local SQLite database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create a table named 'passwords' with 3 columns: ID, Platform Name, and Encrypted Password
        # 'IF NOT EXISTS' ensures we don't accidentally overwrite existing data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                encrypted_password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_password(self, platform: str, password: str):
        # We convert our normal password into an unreadable, locked text using our master key
        encrypted_pw = self.cipher.encrypt(password.encode()).decode()
        
        # Connect to the database and insert the platform name and the locked password
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passwords (platform, encrypted_password) VALUES (?, ?)', (platform, encrypted_pw))
        conn.commit()
        conn.close()

    def get_all_passwords(self):
        # Connect to the database and grab all saved records
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, platform, encrypted_password FROM passwords')
        rows = cursor.fetchall()
        conn.close()
        
        decrypted_passwords = []
        # Loop through every row we grabbed from the database
        for row_id, platform, encrypted_pw in rows:
            try:
                # Unlock the encrypted password back to normal text using our master key
                decrypted_pw = self.cipher.decrypt(encrypted_pw.encode()).decode()
                decrypted_passwords.append((row_id, platform, decrypted_pw))
            except Exception:
                # If unlocking fails (e.g., wrong master key), show an error message instead of crashing
                decrypted_passwords.append((row_id, platform, "Failed to Decrypt!"))
                
        return decrypted_passwords

    def delete_password(self, row_id):
        # Connect to the database and delete the specific row using its unique ID
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM passwords WHERE id = ?', (row_id,))
        conn.commit()
        conn.close()