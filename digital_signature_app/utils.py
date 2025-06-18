# utils.py
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("keys/private_key.pem", "wb") as f:
        f.write(private_key)
    with open("keys/public_key.pem", "wb") as f:
        f.write(public_key)

def sign_file(file_path):
    with open("keys/private_key.pem", "rb") as f:
        private_key = RSA.import_key(f.read())
    with open(file_path, "rb") as f:
        data = f.read()
    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_signature(file_path, signature):
    with open("keys/public_key.pem", "rb") as f:
        public_key = RSA.import_key(f.read())
    with open(file_path, "rb") as f:
        data = f.read()
    h = SHA256.new(data)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
if __name__ == '__main__':
    generate_keys()
