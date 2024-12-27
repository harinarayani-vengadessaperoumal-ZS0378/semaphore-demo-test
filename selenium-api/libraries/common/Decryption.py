import rsa
import base64

class   Decryption:
    
    def load_private_key(self, private_key_string):
        key_data = private_key_string.split(", ")
        n, e, d, p, q = map(int, key_data)
        return rsa.PrivateKey(n, e, d, p, q)

    def decrypt_the_value(self, encrypted_password, privatekey):
        priv_key= self.load_private_key(privatekey)
        enc_passwordinbytes= base64.b64decode(encrypted_password)
        dec_password = rsa.decrypt(enc_passwordinbytes, priv_key).decode()
        print(dec_password)
        return dec_password
