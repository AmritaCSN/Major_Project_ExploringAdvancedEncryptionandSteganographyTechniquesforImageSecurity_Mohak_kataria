import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import time

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc + "========")
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])) 

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

# test_object=AESCipher('12345678')
# print("AES :")
# print("Data Len\tEnc Time\tDec Time")
# for i in range(20):
#     s_time=time.time()
#     message = 'a'*(2**i)
#     encrypted_text=test_object.encrypt(message)
#     dec_time=time.time()-s_time

#     s_time=time.time()
#     decrypted_text=test_object.decrypt(encrypted_text)
#     enc_time=time.time()-s_time

#     print(f"{len(message)}\t{enc_time}\t\t{dec_time}")
