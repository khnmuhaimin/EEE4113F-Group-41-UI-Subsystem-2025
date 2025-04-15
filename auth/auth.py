import hashlib
import os
import secrets
from typing import Any
import argon2

def verify_preshared_key(preshared_key: Any) -> bool:
    """
    Compares the provided preshared key with the expected key from environment variables.

    Args:
        preshared_key (Any): The preshared key to verify.

    Returns:
        bool: True if the provided key matches the environment key, False otherwise.

    Raises:
        KeyError: If the "PRESHARED_KEY" environment variable is not set.
    """
    try:
        return preshared_key == os.environ.get("PRESHARED_KEY")
    except KeyError:
        raise KeyError("Preshared key was not found in the environment variables.")
    

def generate_secret(bytes: int=32) -> str:
    """
    Generates a secure random string.

    Args:
        bytes (int): Number of bytes for the string. Default is 32.

    Returns:
        str: Hexadecimal string.
    """
    return secrets.token_hex(bytes)


def hash_secret(secret: str) -> str:
    """
    Hashes a secret string using SHA-256.

    Args:
        secret (str): The secret to hash.

    Returns:
        str: The hexadecimal SHA-256 hash of the secret.
    """
    return hashlib.sha256(secret.encode()).hexdigest()




def verify_secret(secret: str, hash: str) -> bool:
    """
    Verifies a secret against a given SHA-256 hash.

    Args:
        secret (str): The plain secret to verify.
        hash (str): The SHA-256 hash to compare against.

    Returns:
        bool: True if the hash matches the secret, False otherwise.
    """
    return hash_secret(secret) == hash



def hash_password(password: str) -> str:
    """
    Hashes the provided password using the Argon2 hashing algorithm.
    
    This function uses the default parameters (time_cost, memory_cost, and parallelism)
    of the Argon2 algorithm to securely hash the password. It is suitable for storing
    passwords in a secure format.

    Args:
        password (str): The password to hash.
        
    Returns:
        str: The resulting Argon2 hash of the password, including salt and parameters.
        
    Example:
        hashed_password = hash_password("my_secure_password")
    """
    ph = argon2.PasswordHasher()
    hash = ph.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    """
    Verifies if the provided password matches the stored hash.
    
    This function checks whether the given password corresponds to the provided 
    Argon2 hash. It uses the same parameters (salt, time_cost, memory_cost, etc.) 
    that were used to create the original hash.

    Args:
        password (str): The password to verify.
        hash (str): The stored Argon2 hash to compare against.
        
    Returns:
        bool: True if the password matches the hash, False otherwise.
        
    Example:
        is_valid = verify_password("my_secure_password", stored_hash)
    """
    ph = argon2.PasswordHasher()
    return ph.verify(hash, password)
