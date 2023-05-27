# simple imeplementation of CHACHA20 for encryption and decryption.

import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

class Chacha20(object):
  '''
  This is the custom implementation of chacha20 for encryption and decryption.
  One object corresponds to one {key, noance} set.
  '''
  def __init__(self):
    '''
    no need to define anything, we'll just use the encrypt and decrypt functions
    '''
    pass

  def encrypt(plaintext='plaintext'):
    '''
    This method takes the plaintext and returns the ciphertext alongwith the nonce
    '''
    plaintext = bytes(plaintext, 'utf-8')
    global key # since the same will be used for decryption
    key = get_random_bytes(32) # generate a random key.
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(plaintext)
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ciphertext).decode('utf-8')
    result = json.dumps({'nonce':nonce, 'ciphertext':ct})
    return(result)

  def decrypt(result=''):
    if(result == ''):
      print("Invalid input provided to decrypt")
      return
    enc_b64 = json.loads(result)
    nonce = b64decode(enc_b64['nonce'])
    ciphertext = b64decode(enc_b64['ciphertext'])
    global key
    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return(plaintext.decode("utf-8"))
