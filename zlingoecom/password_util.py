# password_utils.py
import bcrypt
import string
import random




class PasswordUtils:
    @staticmethod
    def encode_password(password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    @staticmethod
    def check_password(encoded_password, user_input_password):
        return bcrypt.checkpw(user_input_password.encode('utf-8'), encoded_password.encode('utf-8'))
    
    @staticmethod
    def custom_encrypt(number):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + "#$%^"
        base = len(characters)
        min_length = 30

        result = ''
        while number > 0 or len(result) < min_length:
            remainder = number % base
            result = characters[remainder] + result
            number = number // base

        if len(result) < min_length:
        
            remaining_chars = min_length - len(result)
            result = result + ''.join(random.choice(characters) for _ in range(remaining_chars))

        return result

    def custom_decrypt(encrypted_text):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + "#$%^"
        base = len(characters)
        result = 0

        for char in encrypted_text:
            result = result * base + characters.index(char)

        return result


