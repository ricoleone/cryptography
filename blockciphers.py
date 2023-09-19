from Crypto.Cipher import DES
scheme = DES.new(b'87654321', DES.MODE_ECB )
ciphertext = scheme.encrypt(b'andyrulz')
print(ciphertext)
print(scheme.decrypt(ciphertext))