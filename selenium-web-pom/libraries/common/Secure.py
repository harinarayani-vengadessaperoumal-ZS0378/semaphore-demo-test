import rsa
import base64

class Secure:

    @staticmethod
    def extract_private_key(private_key_object):

        attributes = ['n','e','d','p','q']
        private_key_string = "-".join([str(getattr(private_key_object,attribute)) for attribute in attributes])
        return private_key_string

    @staticmethod
    def encrypt_password(password):

        public_key, private_key = rsa.newkeys(2048)
        encrypted_password_in_bytes = rsa.encrypt(password.encode(encoding='utf-8'), public_key)
        encrypted_password_in_base64 = base64.b64encode(encrypted_password_in_bytes).decode(encoding='utf-8')
        print(f"Encrypted Password: {repr(encrypted_password_in_base64)}")
        print(f"Private Key: {repr(Secure.extract_private_key(private_key))}") 
        return (encrypted_password_in_base64, Secure.extract_private_key(private_key))

    @staticmethod
    def load_private_key(private_key):

        key_data = private_key.split("-")
        n, e, d, p, q = map(int, key_data)
        return rsa.PrivateKey(n, e, d, p, q)

    @staticmethod
    def decrypt_password(encrypted_password_in_base64, private_key):

        private_key = Secure.load_private_key(private_key)
        encrypted_password_in_bytes= base64.b64decode(encrypted_password_in_base64)
        decrypted_password = rsa.decrypt(encrypted_password_in_bytes, private_key).decode(encoding='utf-8')
        return decrypted_password
