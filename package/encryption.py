import psycopg2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode
import hashlib
import os
import hmac

# Code de mystique de statck overflow 

# Define a function to derive a key from a password using PBKDF2
def derive_key(password):
    # Use PBKDF2 with HMAC-SHA256 to derive the key without a salt
    key = PBKDF2(
        password.encode('utf-8'),
        b'',  # Empty salt
        dkLen=32,  # AES-256 requires a 256-bit key
        count=100000,  # Number of iterations (adjust as needed)
        prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest()
    )
    return key 



# Define the encryption function
def encrypt_AES_CBC_256(key, message):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext_bytes = cipher.encrypt(padded_message)
    ciphertext = b64encode(iv + ciphertext_bytes).decode('utf-8')
    return ciphertext

# Define the decryption function
def decrypt_AES_CBC_256(key, ciphertext):
    ciphertext_bytes = b64decode(ciphertext)
    iv = ciphertext_bytes[:16]  # Extract the IV
    ciphertext_bytes = ciphertext_bytes[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(ciphertext_bytes)
    plaintext_bytes = unpad(decrypted_bytes, AES.block_size)
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext