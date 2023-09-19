
from Crypto.Cipher import AES
from itertools import cycle
import codecs
from base64 import b64encode

######################################################
#         Bytes Conversions Key
# b'\xde\xad\xbe\xef'.hex() -> 'deadbeef'
# bytes.fromhex('deadbeef') -> b'\xde\xad\xbe\xef'
######################################################
def XOR(message, key):
  return ''.join(chr(ord(c)^ord(k)) for c,k in zip(message, cycle(key)))

def XOR2(message, key):
  return ''.join(chr(c^k) for c,k in zip(message, (key)))

def XOR_HS(a, b):
    a_bs = bytes.fromhex(a)
    b_bs = bytes.fromhex(b)
    return bytes(x^y for x,y in zip(a_bs, cycle(b_bs))).hex()

def XOR_BA(a, b):
    return bytes([x^y for x,y in zip(a, cycle(b))])


ct = bytes.fromhex('87dd2acb714db44393d8b4b71bdbad7720fbf40d2e34a03a93324cb9c4b97a08')
print(ct)
print("ct lenght =", len(ct))
ct1 = ct[:16]
ct2 = ct[16:]

key = 'andy love simone'
keybs = key.encode()
print("Key =", keybs)
cipher = AES.new(keybs, AES.MODE_ECB)
otp2 = cipher.decrypt(ct2)
print(otp2, type(otp2))
x_1 = XOR2(otp2, ct1)
print(x_1)
opt1 = cipher.decrypt(ct1)
IV = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
print("IV = ",IV)
iv = IV
x_2 = XOR2(opt1, iv)
print(x_2)

cipher2 = AES.new(keybs, AES.MODE_CBC, IV)
print(cipher2.decrypt(ct))
keybsh = keybs.hex()
print("keybs = ", keybs, " keybs.hex() = ", keybsh)
print("keybsh.bytes.from hex = ", bytes.fromhex(keybsh))

pt = "abcdefghijklmnopqrstuvwxyzabcdef".encode()
print("plain plaintext =", pt)
pt1 = pt[:16]
pt2 = pt[16:]
print("Plaintext first 16 bytes ", pt1)
print("Plaintext second 16 bytes ", pt2)

x_3 = XOR_BA(pt1, iv)
print("Plaintext1 Xor with iv", x_3)
enc1 = cipher.encrypt(x_3)
print(enc1, "length ",len(enc1))
print(enc1.hex())
x_4 = XOR_BA(pt2, enc1)
print("Plaintext2 Xor with encr", x_4)
enc2 = cipher.encrypt(x_4)
print(enc2, "length ",len(enc2))
print(enc2.hex())
