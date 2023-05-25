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

