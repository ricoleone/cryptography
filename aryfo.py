import hashlib
plain_text = 'andy rocks your face off'
print(hashlib.sha512(bytes(plain_text, 'UTF-8')).hexdigest())
