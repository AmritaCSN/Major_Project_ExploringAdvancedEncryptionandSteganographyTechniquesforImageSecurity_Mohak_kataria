import random

class RSA(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.generate_e()
        self.d = self.mod_inv(self.e, self.phi)
        
    def generate_e(self):
        e = random.randint(2, self.phi-1)
        while self.gcd(e, self.phi) != 1:
            e = random.randint(2, self.phi-1)
        return e
    
    def gcd(self, a, b):
        if a == 0:
            return b
        return self.gcd(b % a, a)
    
    def mod_inv(self, a, m):
        for i in range(1, m):
            if (a*i) % m == 1:
                return i
        return -1
    
    def encrypt(self, message):
        ciphertext = []
        for char in message:
            m = ord(char)
            c = ((m ** self.e) % self.n)
            ciphertext.append(str(c))
        return ciphertext
        #print('the value of c:', c)
    
    def decrypt(self, ciphertext):
        plaintext = ""
        for c in ciphertext:
            c = c.replace('[','').replace(']','').replace(',','').replace(' ','') # remove brackets and extra characters
            if not c.isdigit():
                continue
            m = ((int(c) ** self.d) % self.n)
            plaintext += chr(m)
        return plaintext
