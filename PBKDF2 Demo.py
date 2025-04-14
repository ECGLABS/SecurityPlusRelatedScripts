import hashlib
import os
import binascii

# Simulated user password input
password = b"SuperSecretPassword123!"

# Generate a 16-byte random salt
salt = os.urandom(16)
print(f"Salt (hex): {binascii.hexlify(salt).decode()}")

# Derive a cryptographic key using PBKDF2
key = hashlib.pbkdf2_hmac(
    hash_name='sha256',     # Use SHA-256 hash function
    password=password,      # The input password
    salt=salt,              # Salt
    iterations=100_000,     # Number of hashing rounds (stretching!)
    dklen=32                # Desired key length in bytes
)

print(f"Derived Key (hex): {binascii.hexlify(key).decode()}")
