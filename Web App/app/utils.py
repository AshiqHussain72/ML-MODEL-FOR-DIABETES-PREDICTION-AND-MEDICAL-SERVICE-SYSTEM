import random 
def public_key(length):
    sample_string = 'd0LW25jG8feETs4WWpeCUA4AU1oPj7lAcCtKB1Cmuso='
    result = ''.join((random.choice(sample_string)) for x in range(length))
    return result
from cryptography.fernet import Fernet

def generate_fernet_key():
    """
    Generate a Fernet key.
    Returns:
        str: A Fernet key as a URL-safe base64-encoded string.
    """
    return Fernet.generate_key().decode()