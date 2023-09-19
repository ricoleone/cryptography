from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import *
from PIL import Image
from itertools import cycle
import os
import codecs
import secrets
from hashlib import sha256 
from urllib.request import urlopen
from time import sleep

#########################################################################################
# Name:        padding
# Description: Adds padding to the last block of a byte object to prepare for encryption
#              or decryption
# Usage:       pt = padding(pt), where pt = b'something' 
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def padding(pt):
    count = len(pt) % AES.block_size
    padcount = AES.block_size - count
    #pad with integer data whose value is the number of bytes added for padding
    if count > 0:
        pt += padcount.to_bytes(length=1, byteorder='big')*padcount
    return pt
#########################################################################################
# Name:        unpadding
# Description: removes padding to the last block of a byte object to prepare for encryption
#              or decryption
# Usage:       pt = padding(pt), where pt = b'something' 
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def unpadding(pt):
    count = pt[-1]
    tmppt = bytearray(pt)
    if count < AES.block_size and count > 0:
        for i in range(1, count + 1):
            if pt[-i] == count:
                tmppt.pop()
    return bytes(tmppt)
#########################################################################################
# Name:        testpadding
# Description: removes padding to the last block of a byte object to prepare for encryption
#              or decryption
# Usage:       pt = padding(pt), where pt = b'something' 
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def testpadding(pt):
    print("Before padding: ", pt, "length = ", len(pt))
    pt = padding(pt)
    print("After padding added: ", pt, "length = ", len(pt))
    pt = unpadding(pt)
    print("After padding remvoved: ", pt, "length = ", len(pt))
#########################################################################################
# Name: XORS
# Description: returns a string of two hex strings xor'd
# Usage: foo = XOR("0123456789abc", "feeddeadbeef") 
# Author: Rico Leone
# Date: 
#########################################################################################
def XOR_HS(a, b):
    a_bs = bytes.fromhex(a)
    b_bs = bytes.fromhex(b)
    return bytes(x^y for x,y in zip(a_bs, cycle(b_bs))).hex()
#########################################################################################
# Name: XOR2str
# Description: returns a string of two hex strings xor'd
# Usage: foo = XOR("0123456789abc", "feeddeadbeef") 
# Author: Rico Leone
# Date: 
#########################################################################################
def XOR_B2S(message, key):
  return ''.join(chr(c^k) for c,k in zip(message, cycle(key)))
#########################################################################################
# Name: XORB
# Description: returns a byte of two binary stream objects xor'd
# Usage: foo = XOR("0123456789abc", "feeddeadbeef") 
# Author: Rico Leone
# Date: 
#########################################################################################
def XOR_B(a, b):
    return bytes([x^y for x,y in zip(a, cycle(b))])
#########################################################################################
# Name: XORBA
# Description: returns a bytearray of two binary stream objects xor'd
# Usage: foo = XOR("0123456789abc", "feeddeadbeef") 
# Author: Rico Leone
# Date: 
#########################################################################################
def XOR_BA(a, b):
    return bytes([x^y for x,y in zip(a, cycle(b))])

#########################################################################################
# Name: testXOR
# Description: 
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def testXOR():
    a = "deadbeef"
    b = "facefeed"
    c = XOR_HS(a,b)
    print("XOR_HS: ", a," ", b, " ", c)
    print("XOR_HS: bytes from hex ", a," ", b, " ", bytes.fromhex(c))

    e = b"deadbeef"
    f = b"facefeed"
    g = XOR_B(e,f)
    print("XOR_B: ", e," ", f, " ", g)

    h = bytearray().fromhex(a)
    i = bytearray().fromhex(b)
    j = XOR_BA(h,i)
    print("XOR_BA: ", h," ", i, " ", j)

    k = bytes.fromhex('deadbeef')
    l = bytes.fromhex('facefeed')
    m = XOR_B2S(k,l)
    print("XOR_B2S: ", k," ", l, " ", m )

#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def gen_iv(bts=AES.block_size):
    iv = secrets.token_urlsafe()
    tmpiv = iv.encode('utf-8')[:bts]
    return tmpiv, tmpiv.hex()
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def gen_key(bts=256):
    key = secrets.token_urlsafe(bts)
    tmpkey = sha256(key.encode('utf-8'))
    return tmpkey.digest(), tmpkey.hexdigest()
#########################################################################################
# Name:        gen_nonce()
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def gen_nonce(bts=256):
    key = secrets.token_urlsafe(bts)
    tmpkey = sha256(key.encode('utf-8'))
    return tmpkey.digest(), tmpkey.hexdigest()
#########################################################################################
# Name:        gen_counter()
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def gen_counter(bts=int(AES.block_size/2)): 
    return b'0'*bts
#########################################################################################
# Name:        gen_counter()
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def inc_counter(b):
    counter  = bytes_to_long(b)
    counter +=1
    return long_to_bytes(counter)
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def testkeys():
    key = gen_key()
    IV = gen_iv()
    print("key = ", key, "type = ", type(key), "size = ", len(key))
    print("IV = ", IV, "type = ", type(IV), "size = ", len(IV))
        
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def gen_AES(key, mode=AES.MODE_ECB, IV=b''):
    scheme = AES
    if IV == b'':
        scheme = AES.new(key, mode)
    else:
        scheme = AES.new(key, mode, iv=IV)
    return scheme
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def gen_AES_lazy(mode=AES.MODE_ECB):
    key = gen_key()
    IV  = gen_iv()
    scheme = AES.new(key, mode, iv=IV) 
    return key, IV, scheme
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def decrypt_IMG(im, key, mode, IV=b''):
    scheme = AES
    if IV == b'':
        scheme = gen_AES(key, mode)
    else:
        scheme = gen_AES(key, mode, IV)
    return unpadding(scheme.decrypt(padding(im.tobytes())))
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def encrypt_IMG(im, key, mode, IV=b''):
    scheme = AES
    if IV == b'':
        scheme = gen_AES(key, mode)
    else:
        scheme = gen_AES(key, mode, IV)
    return scheme.encrypt(padding(im.tobytes()))
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def testECB(filename = "Boston-Bruins-logo-700x394.png"):
        save_to = "RL_ECB_ne.png"
        mode = AES.MODE_ECB
        key  = bytes.fromhex('4c6bcaccb1ef923e1ddcce50720dbd7dba0f71d84436cc5651e2d040e0ebd9e7')
        print(key)
        im = Image.open(filename)
        im.show()
        print(im.format, im.size, im.mode)
        print("AES.block_size Bytes = ", AES.block_size)
        print("Image Bytes = ", im.size[0]*im.size[1])
        print("Image Bytes % AES.block_size ", (im.size[0]*im.size[1]) % AES.block_size)
        im.frombytes(encrypt_IMG(im, key, mode))
        im.show()
        sleep(3)
        im.save(save_to)
        im2 = Image.open(save_to)
        print(im2.format, im2.size, im2.mode)
        im2.frombytes(decrypt_IMG(im2, key, mode))
        im2.show()
        sleep(3)
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def testCBC(filename = "Boston-Bruins-logo-700x394.png"):
        mode = AES.MODE_CBC
        save_to  = "RL_CBC_enc.png"
        key, hexkey = gen_key()
        iv, hexiv   = gen_iv()
        print("key = ", key)
        print("key(hex) = ", hexkey)
        print("iv = ", iv)
        print("iv(hex) = ", hexiv)
        im = Image.open(filename)
        im.show()
        print(im.format, im.size, im.mode)
        print("AES.block_size Bytes = ", AES.block_size)
        print("Image Bytes = ", im.size[0]*im.size[1])
        print("Image Bytes % AES.block_size ", (im.size[0]*im.size[1]) % AES.block_size)
        print(filename)
        print("encrypting image:")
        im.frombytes(encrypt_IMG(im, key, mode, iv))
        im.show()
        sleep(3)
        ("Opening encrypted image:")
        print("decrypting image:")
        im.frombytes(decrypt_IMG(im, key, mode, iv))
        im.show()
#########################################################################################
# Name:        my_CBC_encrypt
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_CBC_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def my_CBC_enc(mes, key, iv):
    key = key.encode()
    IV  = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_ECB)
    pt  = mes.encode()
    pt  = padding(pt)
    input  = b''
    output = b''
    ct = b''
    prevct = IV
    for block in range(0, len(pt), AES.block_size):
        input  = XOR_BA(pt[block:(block + AES.block_size)], prevct)
        output = cipher.encrypt(input)
        ct    += output
        prevct = output
    return ct
#########################################################################################
# Name:        my_CBC_decrypt
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_CBC_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def my_CBC_dec(mes, key, iv):
    key = key.encode()
    IV  = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_ECB)
    ct  = mes
    input  = b''
    output = b''
    pt = b''
    prevct = IV
    for block in range(0, len(ct), AES.block_size):
        input  = ct[block:(block + AES.block_size)]
        output = cipher.decrypt(input)
        pt += XOR_BA(output, prevct)
        prevct = input
    return unpadding(pt)
#########################################################################################
# Name:        testmy_CBC
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_CBC_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################    
def testmy_CBC():
    KEY     = 'andy love simone'
    IV      = "000102030405060708090a0b0c0d0e0f"
    MESSAGE = "abcdefghijklmnopqrstuvwxyzabcdef"
    print("Testing my_CBC:\nkey     = ", KEY, "\nIV      = ", IV, "\nMESSAGE = ", MESSAGE)
    ct = my_CBC_enc(MESSAGE, KEY, IV)
    print("Ciphter text = ", ct.hex())
    if ct.hex() == '87dd2acb714db44393d8b4b71bdbad7720fbf40d2e34a03a93324cb9c4b97a08':
        print("my_CBC encryption test passed!")
    pt = my_CBC_dec(ct, KEY, IV)
    print("Plain text = ", pt)
    if pt == MESSAGE.encode():
        print("my_CBC decryption test passed!")

#########################################################################################
# Name:        my_OFB_encrypt
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_OFB_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def my_OFB_enc(mes, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    pt     = padding(mes)
    input  = b''
    output = b''
    ct     = b''
    input  = iv
    for block in range(0, len(pt), AES.block_size):
        output = cipher.encrypt(input)
        input  = output
        ct += XOR_BA(pt[block:(block + AES.block_size)], output)
    return ct
#########################################################################################
# Name:        my_OFB_decrypt
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_OFB_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def my_OFB_dec(mes, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    ct     = mes
    input  = b''
    output = b''
    pt     = b''
    input = iv
    for block in range(0, len(ct), AES.block_size):
        output = cipher.encrypt(input)
        input  = output
        pt += XOR_BA(ct[block:(block + AES.block_size)], output)
    return unpadding(pt)
#########################################################################################
# Name:        testmy_OFB
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_CBC_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################    
def testmy_OFB():
    KEY     = b'andy love simone'
    IV      = b"Not very random."
    MESSAGE = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    print("Testing my_OFB:\nkey     = ", KEY, "\nIV      = ", IV, "\nMESSAGE = ", MESSAGE)
    ct = my_OFB_enc(MESSAGE, KEY, IV)
    print("Ciphter text = ", ct.hex())
    if ct.hex() == '4e6f7420766572792072616e646f6d2e91de0aa207cf9f7d0f3cdf245e88f281248b5a2d4cb1b3afefac7bd25c1bc90a177fb88bea185fe13e766cd60a011c20e108f6a8693c756a70da283af3604fb3'[32:]:
        print("my_OFB encryption test passed!")
    pt = my_OFB_dec(ct, KEY, IV)
    print("Plain text = ", pt)
    if pt == MESSAGE:
        print("my_OFB decryption test passed!")
#########################################################################################
# Name:        my_CTR_encrypt
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_CTR_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def my_CTR_enc(mes, key):
    cipher = AES.new(key, AES.MODE_ECB)
    pt     = mes
    input  = b''
    output = b''
    ct     = b''
    nonce, hexnonce = gen_nonce()
    nonce  = nonce[:8]
    counter = gen_counter()
    input  = nonce + counter
    for block in range(0, len(pt), AES.block_size):
        output = cipher.encrypt(input)
        ct += XOR_BA(pt[block:(block + AES.block_size)], output)
        counter = inc_counter(counter)
        input = nonce + counter
    return ct, nonce
#########################################################################################
# Name:        my_CTR_decrypt
# Description: Takes plaintext message, hex string key, and hexstring iv to encrypt the 
#              message. Returns ciphertext as bytes. Assumes message is plaintext, and
#              key and iv are hex strings. 
# Usage:       my_CTR_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def my_CTR_dec(ct, key, nonce):
    cipher = AES.new(key, AES.MODE_ECB)
    output = b''
    pt     = b''
    tmpnonce  = nonce
    counter = gen_counter()
    input  = tmpnonce + counter
    for block in range(0, len(ct), AES.block_size):
        output = cipher.encrypt(input)
        pt += XOR_BA(ct[block:(block + AES.block_size)], output)
        counter = inc_counter(counter)
        input = nonce + counter
    return pt
#########################################################################################
# Name:        testmy_CTR
# Description: 
# Usage:       my_CTR_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def testmy_CTR():
    KEY     = b'andy love simone'
    IV      = b"Not very random."
    MESSAGE = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    print("Testing my_CTR:\nkey     = ", KEY, "\nIV      = ", IV, "\nMESSAGE = ", MESSAGE)
    ct, nonce = my_CTR_enc(MESSAGE, KEY)
    print("Ciphter text = ", ct.hex())
    if ct.hex() == '4e6f7420766572792072616e646f6d2e91de0aa207cf9f7d0f3cdf245e88f281248b5a2d4cb1b3afefac7bd25c1bc90a177fb88bea185fe13e766cd60a011c20e108f6a8693c756a70da283af3604fb3'[32:]:
        print("my_CTR encryption test passed!")
    pt = my_CTR_dec(ct, KEY, nonce)
    print("Plain text = ", pt)
    if pt == MESSAGE:
        print("my_CTR decryption test passed!")
#########################################################################################
# Name:        testmy_CTR_IMG
# Description: 
# Usage:       my_CTR_encrypt(message, key, IV)
# Author:      Rico Leone
# Date:        3/12/2023
#########################################################################################
def testmy_CTR_IMG(filename = "Boston-Bruins-logo-700x394.png"):
        mode = AES.MODE_CBC
        save_to  = "RL_CTR_enc.png"
        key, hexkey = gen_key()
        print("key = ", key)
        print("key(hex) = ", hexkey)
        im = Image.open(filename)
        im.show()
        print(im.format, im.size, im.mode)
        print("AES.block_size Bytes = ", AES.block_size)
        print("Image Bytes = ", im.size[0]*im.size[1])
        print("Image Bytes % AES.block_size ", (im.size[0]*im.size[1]) % AES.block_size)
        print(filename)
        print("encrypting image:")
        cleardata = im.tobytes()
        ct, nonce = my_CTR_enc(im.tobytes(), key)
        im.frombytes(ct)
        im.show()
        sleep(3)
        print("Opening encrypted image:")
        print("decrypting image:")
        pt = my_CTR_dec(ct, key, nonce)
        im.frombytes(pt)
        im.show()
        if cleardata == pt:
            print("TEST my_CTR_IMG passed!")
#########################################################################################
# Name: 
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def testCFB(filename = "Boston-Bruins-logo-700x394.png"):
        mode = AES.MODE_CBC
        #key  = bytes.fromhex('910d2d9485c3dcef7f3b523fc7fbb6e40c7a021f84410dc91159a104d9f52e94')
        #iv = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
        encryptedfile  = "RL_CBC_enc.png"
        key, hexkey = gen_key()
        iv, hexiv   = gen_iv()
        print("key = ", key)
        print("iv = ", iv)
        im = Image.open(filename)
        im.show()
        print(im.format, im.size, im.mode)
        print("encrypting image file :", filename)
        im.frombytes(encrypt_IMG(im, key, mode, iv))
        im.show()
        im.save(encryptedfile)
        sleep(3)
        ("Opening encrypted image:")
        im2 = Image.open(encryptedfile)
        im2.show()
        print(im2.format, im2.size, im2.mode)
        print("Image Bytes = ", im2.size[0]*im2.size[1])
        print("Image Bytes % AES.block_size ", (im2.size[0]*im2.size[1]) % AES.block_size)
        print("decrypting image:")
        im2.frombytes(decrypt_IMG(im2, key, mode, iv))
        im2.show()
        sleep(3)
        im3 = Image.open(filename)
        padding = b''
        if (im.size[0]*im.size[1]) % AES.block_size > 0:
            padding += b'0'*(AES.block_size - (im.size[0]*im.size[1]) % AES.block_size)
        if (im3.tobytes() + padding) == im2.tobytes():
            print("CFB Cipher Test was a Success!")
#########################################################################################
# Name:        testOFB
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def testOFB():
        mode = AES.MODE_OFB
        #test with Andy's key and IV
        message  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.encode()
        key  = 'andy love simone'.encode()
        iv = 'Not very random.'.encode()
        print("Building OFB cipher with:")
        print("key = ", key)
        print("iv  = ", iv)
        cipher = AES.new(key, AES.MODE_OFB, iv)
        ct = cipher.encrypt(message)
        cipher2 = AES.new(key, AES.MODE_OFB, iv)
        pt = cipher2.decrypt(ct)
        if pt == message:
            print("Test OFB MODE SUCCESSFULL!")
            print("The plaintext is: ", pt)
#########################################################################################
# Name:        download_IMG
# Description: Downloads an image file from an URL and saves it to disk using the image 
#              filename. Assumes the image is binary format and has the appropriate 
#              for the file type extension. Returns the file name of the save image.
# Usage:       filename = downloag_IMG(URL)
# Author:      Rico Leone
# Date: 
#########################################################################################
def download_IMG(url):
    saved_to = url.strip('/').split('/')[-1]
    data =b''
    try:
        with urlopen(url) as f:
            data = f.read()
    except ConnectionRefusedError:
        print("Connection to ", url, " Refused")
    try:
        with open(saved_to, 'wb') as f:
            f.write(data)
    except IOError:
        print("File, ", "'", saved_to, "'", "already exists")
    return saved_to

#########################################################################################
# Name: Main
# Description:
# Usage: 
# Author: Rico Leone
# Date: 
#########################################################################################
def main():
    #  url = input("Enter the URL of an image file: ")
    #  print("the image has been saved as ", download_IMG(url) )
    TEST = True
    if TEST:
        # Uncomment the test you want to run some encrypt and or decryt files, others are unit test and 
        # one or two encrypt/decrypt examaples from class.
        print("Currently in Test mode.")
        #  url = input("Enter the URL of an image file: ")
        #  print("the image has been saved as ", download_IMG(url) )

        # testpadding(pt = b'aaaabbbbcccc')
        # testkeys()
        # testXOR()
        # testECB()
        # testCBC()
        # testCFB()
        # testOFB()
        # testmy_CBC()
        # testmy_OFB()
        # testmy_CTR()
        testmy_CTR_IMG()
#use the section to run images from classmates, by setting TEST to False
    else:
        filename ="wu_CBC_image.png"
        save_to  = "output.png"
        key  = bytes.fromhex('0123456789abcdef0123456789abcdef')
        iv = bytes.fromhex('fedcba9876543210fedcba9876543210')
        mode = AES.MODE_CBC
        im = Image.open(filename)
        print(im.format, im.size, im.mode)
        print("Image Bytes = ", im.size[0]*im.size[1])
        print("Image Bytes % AES.block_size ", (im.size[0]*im.size[1]) % AES.block_size)
        im.show()
        sleep(3)
        im.frombytes(decrypt_IMG(im,key,mode,iv))
        im.show()
        im.save(save_to)
    print("Done encrypting /decrypting images!") 
    return (0)

if __name__ == "__main__":
    main()