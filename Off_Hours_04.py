from Crypto.Cipher import AES

key = b'andy love simone'

print(len(key))

cipher = AES.new(key, AES.MODE_ECB)

print(cipher)

enc = cipher.encrypt(b'andy love simone')
print(enc)

denc = cipher.decrypt(enc)

print(denc)