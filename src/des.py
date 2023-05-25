from Crypto.Cipher import DES
import time
import textwrap
import base64
import hashlib
from Crypto import Random



class DESCipher(object):

    def __init__(self, key):
        self.bs = 8
        self.key = key.encode('UTF-8')

    def encrypt(self, raw):
        raw = self._pad(raw)
        # iv = Random.new().read(AES.block_size)
        cipher = DES.new(self.key, DES.MODE_CFB)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc + "========")
        cipher = DES.new(self.key, DES.MODE_CFB)
        return self._unpad(cipher.decrypt(enc))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

# test_object=DESCipher('12345678')
# print("DES :")
# print("Data Len\tEnc Time\tDec Time")
# for i in range(20):
#     s_time=time.time()
#     message = 'a'*(2**i)
#     encrypted_text=test_object.encrypt(message)
#     dec_time=time.time()-s_time

#     s_time=time.time()
#     decrypted_text=test_object.decrypt(encrypted_text)
#     enc_time=time.time()-s_time
#     # debug
#     # print(f"Encr Text {encrypted_text} == dec text = {decrypted_text}")
#     print(f"{len(message)}\t{enc_time}\t\t{dec_time}")
