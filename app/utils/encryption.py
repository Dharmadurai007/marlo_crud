from cryptography.fernet import Fernet
from config import Config

key = Fernet(Config.ED_SECRET_KEY)

def encrypt(data):
    encrypted_data = key.encrypt(data.encode('utf-8'))
    return str(encrypted_data)
    
def decrypt(data):
    decrypted_data = key.decrypt(eval(data.encode('utf-8')))
    return decrypted_data.decode('utf-8')