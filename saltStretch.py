import hashlib, bcrypt, random

f = open('dictionary.txt','r')
words = [word.strip() for word in f]
f.close()

salt = bcrypt.gensalt()
index = random.randint(0, len(words) - 1)
secret = bytes(words[index], 'UTF-8')
r = 256
#example values from class
#r = 256
#secret = b'pass1234'
#salt = b'somesalt'
#r = 3
print("The secret is ", secret)
print("The salt value is ", salt)
print("The stretch value is ", r)

#pw is a byte encoded password and salt is a byte encrypted salt
def saltedSHA256(pw, salt):
  return hashlib.sha256(pw  + salt).digest()

  #r is the stretch factor
def stretchSHA256(salt, pw, r):
  xi = b'0'
  for i in range(r): 
    xi =  saltedSHA256((xi + pw), salt)
  return xi

print(stretchSHA256(salt, secret, r))