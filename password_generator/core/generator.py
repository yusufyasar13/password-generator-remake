import string
import secrets

class PasswordGenerator:
    def __init__(self):
        # We define the characters that can be used in the password.
        # string.ascii_letters contains all lowercase and uppercase letters (a-z, A-Z)
        self.letters = string.ascii_letters
        # string.digits contains numbers from 0 to 9
        self.digits = string.digits
        # string.punctuation contains symbols like !@#$%^&*
        self.symbols = string.punctuation

    def generate(self, length: int, use_letters: bool, use_digits: bool, use_symbols: bool = False) -> str:
        """
        Generates a cryptographically secure random password based on user choices.
        """
        pool = "" # This is an empty bucket. We will throw our selected characters inside it.
        
        # If the user wants letters, add letters to our bucket
        if use_letters:
            pool += self.letters
        # If the user wants numbers, add numbers to our bucket
        if use_digits:
            pool += self.digits
        # If the user wants symbols, add symbols to our bucket
        if use_symbols:
            pool += self.symbols
            
        # If the user selected nothing and the bucket is empty, we must warn them!
        if not pool:
            raise ValueError("You must select at least one character type to generate a password!")

        # 'secrets.choice' picks a random character from our bucket.
        # We repeat this action 'length' times to build the final password.
        # Using 'secrets' instead of 'random' makes it impossible for hackers to predict the password.
        password = ''.join(secrets.choice(pool) for _ in range(length))
        
        return password