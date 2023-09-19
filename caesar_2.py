import random

f = open('dictionary.txt','r')
words = [word.strip() for word in f]
f.close()

index = random.randint(0, len(words) - 1)
secret = words[index]
radix = random.randint(0,25)
print("The secret is ", secret)
print('radix = ', radix)

def encrypt(secret, radix):
  ct = ''
  for letter in secret:
    ct += chr((ord(letter) - ord('a') + radix + 26)%26 + ord('a'))
  return ct


def decrypt(ct, radix):
  pt = ''
  for letter in ct:
    pt += chr((ord(letter) - ord('a') - radix + 26)%26 + ord('a'))
  return pt

cipherText = encrypt(secret, radix)
print('cipher text =', cipherText )
plainText = decrypt(cipherText, radix)
print('plain text =', plainText)
if secret == plainText:
  print('winner winner chicken dinner')
  