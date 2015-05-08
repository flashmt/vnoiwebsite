import base64
from Crypto.Cipher import AES

from django.contrib.auth.models import Group


def is_admin(user):
    return Group.objects.get(name="Admin") in user.groups.all()

# Utility functions for encryption and decryption

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = chr(10)

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

def encrypt(key, message):
    cipher = AES.new(pad(key)[::-1])
    encrypted_message = base64.b64encode(cipher.encrypt(pad(message)))
    return encrypted_message


def decrypt(key, encrypted_message):
    cipher = AES.new(pad(key)[::-1])
    message = cipher.decrypt(base64.b64decode(encrypted_message)).rstrip(PADDING)
    return message
