import hashlib
file = open('dictionary.txt', 'r')
words = [word.strip() for word in file]
file.close()
file2 = open('secret', 'r')
secret = file2.read()
file2.close()
print(secret)
for word in words:
  if hashlib.sha512(bytes(word, 'UTF-8')).hexdigest() == secret:
     print('The secret word is ', word)
     break