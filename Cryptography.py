from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generate RSA Key Pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Message to be signed
message = b"This is a secure message that needs verification."

# Sign the message using private key
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Verify the signature using public key
def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("✅ Signature is valid. Message integrity verified.")
    except Exception as e:
        print("❌ Signature is invalid. Message may have been tampered with.")

# Run verification
verify_signature(public_key, message, signature)

# Try tampering
tampered_message = b"This is a secure message that has been hacked."
verify_signature(public_key, tampered_message, signature)
