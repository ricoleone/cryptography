####################################################################
# Create CBC Mode by chaining EBC mode encryption
####################################################################
from Crypto.Cipher import AES
import Crypto.Util.strxor as sxo
key = b'andy love simone'

#CBC Mode 
ciphercbc = AES.new(key, AES.MODE_CBC, b'\x10'*16)
ct = ciphercbc.encrypt(b'andy love simoneandy love simone')
print(ct)

#ECB Mode
simplecipher = AES.new(key, AES.MODE_ECB)
ct2 = b''
IV=b'\x10'*16
pt1 = b'andy love simone'
#ECB 1
ecb_in_01 = sxo.strxor(IV,pt1)
print(ecb_in_01)
ecb_out_01 = simplecipher.encrypt(ecb_in_01)
print(ecb_out_01)
ecb_in_02 = sxo.strxor(ecb_out_01, b'andy love simone')
print(ecb_in_02)
ecb_out_02 = simplecipher.encrypt(ecb_in_02)
print(ecb_out_02)