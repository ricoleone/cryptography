from itertools import permutations
import time, random

# column encryt from Andy
def col_trans(plain):
    cols = int(9) #random.randint(8,10)
    key = range(cols)
    key = random.sample(key, k=len(key))
    #print("KEY TYPE", type(key))
    return "".join(plain[i::cols].upper() for i in key), key


#######################################################################################
# col_decrypt(ciphertext, key)
######################################################################################
def col_decrypt(cipher, key):
  cols = len(key)
  rows = int(len(cipher)/cols)
  #separate cipher into coluns
  columns = [cipher[i*rows:i*rows + rows ] for i in range(cols)]
  #reorder columns back to the original order
  tmp = [''] * cols
  j = 0
  for i in key:
    tmp[i] = columns[j]
    j +=1
  columns = tmp
  #columns = [insert(key, x) ]
  #create the plain text by reading across rows
  # read across each row to get the plaintext
  pt = ""
  for row in range(rows):
    for column in range(cols):
      pt += columns[column][row]
  return pt

#######################################################################################
# Name: encryp
#######################################################################################

def encrypt(plaintext, key):
    ciphertext = [''] * len(key)
    
    for column in range(len(key)):
      char = column
      while char < len(plaintext):
        ciphertext[column] += plaintext[char]
        char += len(key)
    
    #shuffle columns to be in alphabetical order of the key
    alphaOrder = ''.join(sorted(key))
    finalciphertext = [''] * len(key)
    for i in range(len(key)):
      for j in range(len(key)):
        if alphaOrder[i] == key[j]:
          finalciphertext[i] = ciphertext[j]
    
    return ''.join(finalciphertext)
#######################################################################################
# Name: decrypt
#######################################################################################
def decrypt(ct, key):
  print("key in decrypt ", key)
  #print("key type ", type(key))
  keysize = len(key)
  blocksize = int(len(ct)/keysize) 
  ciphertext = [''] * keysize
  #read blocks of text representing columns
  for block in range(keysize):
    ciphertext[block] = ct[block * blocksize: block * blocksize + blocksize ]
  
  #shuffle columns to be realigned with the key order
  alphaOrder = ''.join(sorted(key))
  print("alphaOreder =", alphaOrder)
  finalciphertext = [''] * len(key)
  for i in range(len(key)):
    for j in range(len(key)):
      if key[i] == alphaOrder[j]:
        finalciphertext[i] = ciphertext[j]
        
  # read across each row to get the plaintext
  plaintext = ""
  for row in range(blocksize):
    for column in range(keysize):
      plaintext += finalciphertext[column][row]
  return plaintext


####################################################################################
# Name: fitness
#
####################################################################################
def fitness(plaintext):
  ptlen = len(plaintext)
  words = ["THE", "MAN", "MEN", "AND", "ING", "ENT", "ION", "HER", "FOR", "ONE", "THIS", "FIGHT", "COUNTRY", "LIBERTY", "DEATH", "LIVE"]
  score = 0
  for word in words:
    wordlen = len(word)
    for i in range(ptlen - wordlen):
      snippet = plaintext[i : i + wordlen]
      if snippet == word:
        score += wordlen**2
  return score

####################################################################################
# Name: test
# Description: test the columnar decrypt and encrypt functions
####################################################################################
def test(plaintext = "THISISASHORTBLOCKOFTEXTTOSEEIFIGOTITRIGHTSNOWFOOBA", key = "42031"):
  
  ct, ck = col_trans(plaintext)
  #print("ct = ", ct)
  #print("ck key =", ck)
  #print("ck type ", type(ck))
  temp = ""
  for i in ck:
    temp += chr(i + ord('0'))
  print("tmp= ", temp)
  key = temp
  pt = col_decrypt(ct, ck)
  print("plaintext = ", plaintext)
  print("ct =        ", ct)
  print("pt =        ", pt)
  print("fitness score = ",fitness(pt))
  if plaintext == pt:
    return True
  return False

####################################################################################
# Name: solve
# Description: Solve the Black Hat Challenge for Columnar encoded text with no
#              punctuation and no spaces, all the same case.
# Usage:       solve(ciphtertex, key)
#                cypertext: a string of upper case letters with no spaces
#                key: a string of all ten digits from 0 to 9 in any order
# Output:      writes the top fitness scores and corresponding key value to
#              the file "mostfit.txt" in the current directory
####################################################################################
def solve(ciphertext):
  keys = permutations(range(9))
  bestkey = ""
  highscore = 0
  solved = ""
  for key in list(keys):
    #key =  "".join(i)
    pt = col_decrypt(ciphertext, key)
    score = fitness(pt)
    if score > highscore:
      highscore = score
      bestkey = key
      solved  = pt
      
  print("high score: ", highscore, "key: ", bestkey)
  print(solved)
  

#print("testing solve")

#pt = "THISISASHORTBLOCKOFTEXTTOSEEIFIGOTITRIGHTSNOWFOOBARLIBERTYME"
#pt = "nxhvbvkqyfxgzzmrgkgjqwrqrqdizzrcrpublrizptbvrckgsunalszixdbvgdquagbeqqhm"
#pt = pt.upper()
#print("plaint text lenght = ", len(pt) )
#key = "6140873952"
#ct, ck = col_trans(pt)
#starttime = time.time()
#solve(ct)
#endtime = time.time()
#print("elapsed time: ", endtime - starttime)
#print("pt      = ", pt)
#print("ct      = ", ct)
#print("ck      = ", ck)

#print("running test")
#starttime= time.time()
#test()
#endtime = time.time()
#print("elapsed time: ", endtime - starttime)
columns = [ "one", "two", "three", "four"]
#tmp = [''] * len(columns)
key = [ 3, 2, 0, 1]
tmp = [ columns[k] for k in key]
print(columns)
print(tmp)
print([[x for x in range(3)] for y in range(4)])