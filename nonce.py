#######################################################################
# Name: nonce
# Author: Prof. Andy Novocin, Uninersity of Delaware
# Decscription: Modified for Python3
########################################################################
from itertools import cycle
from Crypto.Util.number import *
import hashlib
import os
import string
#from secret import key, flag

def generate_seed(secret, nonce):
    return bytes_to_long(hashlib.sha256(nonce + secret).digest()) % 2**32

def crand(seed):
    r=[]
    r.append(seed)
    for i in range(30):
        r.append((16807*r[-1]) % 2147483647)
        if r[-1] < 0:
            r[-1] += 2147483647
    for i in range(31, 34):
        r.append(r[len(r)-31])
    for i in range(34, 344):
        r.append((r[len(r)-31] + r[len(r)-3]) % 2**32)
    while True:
        next = r[len(r)-31]+r[len(r)-3] % 2**32
        r.append(next)
        yield (next >> 1 if next < 2**32 else (next % 2**32) >> 1)

def generate_byte_array(seed, num_bytes):
  generator = crand(seed)
  return [generator.next() % 256 for _ in range(num_bytes)]

def XOR(message, key):
  return ''.join(chr(ord(c)^ord(k)) for c,k in zip(message, cycle(key)))

def encrypt(plaintext, secret):
  nonce = os.urandom(6)
  thisseed = generate_seed(secret, nonce)
  thiskey = generate_byte_array(thisseed, len(plaintext))
  ct = nonce
  for i in range(len(plaintext)):
    ct += chr(ord(plaintext[i]) ^ thiskey[i])
  return ct

def decrypt(ciphertext, secret):
  nonce = ciphertext[:6]
  encrypted_message = ciphertext[6:]
  thisseed = generate_seed(secret, nonce)
  thiskey = generate_byte_array(thisseed, len(encrypted_message))
  pt = ''
  for i in range(len(encrypted_message)):
    pt += chr(ord(encrypted_message[i]) ^ thiskey[i])
  return pt

def main():
    print("running ...")
    nonce = os.urandom(6)
    print(repr(string.printable))
    # print(encrypt(string.printable, key, nonce).encode('hex'))
    # print(encrypt(flag, key, nonce).encode('hex'))
    #ipython ctf.py > output.txt
    message = "This is a SUPER SECRT message yo."
    key = "banana salmon"
    ct = encrypt(message, key)
    print(ct)

if __name__ == "__main__":
    main()