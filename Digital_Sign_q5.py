from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

document = b"Blockchain Developer"

signature = private_key.sign(document, padding.PKCS1v15(), hashes.SHA256())

print(f"Document  : {document.decode()}")
print(f"Signature : {signature.hex()}\n")

try:
    public_key.verify(signature, document, padding.PKCS1v15(), hashes.SHA256())
    print("Verification: SUCCESS - Signature is valid.")
except Exception:
    print("Verification: FAILED - Signature is invalid.")
