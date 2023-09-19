import random

f = open('dictionary.txt','r')
words = [word.strip() for word in f]
f.close()

index = random.randint(0, len(words) - 1)
secret = words[index]
radix = random.randint(0,25)
print("The secret is ", secret)
print('radix = ', radix)

# make a list of numbers from 97-123 and then map(convert) it into # characters. 
alpha_list = list(map(chr, range(97, 123)))

#encrypt
ct = ''
for letter in secret:
  #index = ord(letter) - ord('a')
  #index = (index + radix )%26
  #ct += alpha_list[index]
  ct += chr((ord(letter) - ord('a') + radix + 26)%26 + ord('a'))
print('cipher text =', ct)

#decrypt
pt = ''
for letter in ct:
  #index = ord(letter) - ord('a')
  #index = (index - radix + 26)%26
  #pt += alpha_list[index]
  pt += chr((ord(letter) - ord('a') - radix + 26)%26 + ord('a'))
print('plain text =', pt)
if secret == pt:
  print('winner winner chicken dinner')
  
