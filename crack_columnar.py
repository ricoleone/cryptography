from itertools import permutations
import time, random
from datetime import datetime

# column encryt from Andy
def col_trans(plain,ksize):
    cols = int(ksize) #random.randint(8,10)
    key = range(ksize)
    key = random.sample(key, ksize)
    # print("KEY TYPE", type(key))
    return "".join(plain[i::cols].lower() for i in key), key


#######################################################################################
# col_decrypt(ciphertext, key)
######################################################################################
def col_decrypt(cipher, key):
  cols = len(key)
  rows = int(len(cipher)/cols)
  # separate cipher into coluns
  columns = [cipher[i*rows:i*rows + rows ] for i in range(cols)]
  # reorder columns back to the original order based on digits in key
  # where the value of each key digit maps the index of the current 
  # ciphertext column to its index in plaintext
  tmp = [''] * cols
  j = 0
  for i in key:
    tmp[i] = columns[j]
    j +=1
  columns = tmp
  #columns = [columnd[j] for]
  # create the plain text by reading across rows
  # read across each row to get the plaintext
  pt = ""
  for row in range(rows):
    for column in range(cols):
      pt += columns[column][row]
  return pt.upper()

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
    
    # shuffle columns to be in alphabetical order of the key
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
  # print("key type ", type(key))
  keysize = len(key)
  blocksize = int(len(ct)/keysize) 
  ciphertext = [''] * keysize
  # read blocks of text representing columns
  for block in range(keysize):
    ciphertext[block] = ct[block * blocksize: block * blocksize + blocksize ]
  
  # shuffle columns to be realigned with the key order
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
def fitness(ptext):
  ptlen = len(ptext)
  # f = open('top100.txt','r')
  # words = [word.strip() for word in f]
  # f.close()
  # "BE", "TO", "OF",
  words = ["THE", "MAN", "MEN", "AND", "ING", "ENT", "HIS", "HER", 
  "FOR", "ONE", "TION", "SION", "THAT", "WITH","THIS", "FROM", "HAVE", "THEY", "WERE", "BEEN",  "WERE", 
  "THEN", "NEVER", "ALWAYS", "SOME", "LIKE", "MOST", "KNOW"]
  score = 0
  for word in words:
    wordlen = len(word)
    for i in range(ptlen - wordlen):
      snippet = ptext[i : i + wordlen]
      if snippet == word:
        score += wordlen**2
  return score

####################################################################################
# Name: test
# Description: test the columnar decrypt and encrypt functions
####################################################################################
def test(plaintext = "THISISASHORTBLOCKOFTEXTTOSEEIFIGOTITRIGHTSNOWFOOBA", ksize = 5):
  
  ct, ck = col_trans(plaintext, ksize )
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
def solve(ciphertext, ksize):
  f = open("Colunmar-scores_BH02.csv", "w")
  highscore = 0
  bestkey = range(ksize)
  solved  = ""
  count = 0
  
  # loop through all permutations
  keys = permutations(range(ksize))
  for key in list(keys):
    count +=1
    pt = col_decrypt(ciphertext, key)
    score = fitness(pt)
    
    # track the high scores
    if score > highscore:
      highscore = score
      bestkey = key
      solved  = pt
      f.write(str(score) + ", " + str(key) + ", " + pt + "\n")
    else:
         if (score == highscore) | (score > (highscore*(0.9))):
            f.write(str(score) + ", " + str(key) + ", " + pt + "\n")

  print("count: ", count, "high score: ", highscore, "key: ", bestkey)
  print(solved)
  
# run or test the code
SOLVE = True
TEST  = not SOLVE
pt = "THISISASHORTBLOCKOFTEXTTOSEEIFIGOTITRIGHTSNOWFOOBARLIBERTYME"
if SOLVE:
  print("Sovle started at ", datetime.now().strftime('%A %d-%m-%Y, %H:%M:%S'))
  f = open('BlackHatChallenge_02.txt', 'r')
  ct = f.read()
  padding = ''
  ct += padding
  print("cipher text length = ", len(ct) )
  print("first char = ", ct[0])
  print("ciphertext:\n", ct, "\n")
  starttime = time.time()
  solve(ct, 8)
  endtime = time.time()
  print("elapsed time: ", endtime - starttime)
else:
  if TEST:
    print("test started at ", datetime.now().strftime('%A %d-%m-%Y, %H:%M:%S'))
    starttime= time.time()
    test()
    endtime = time.time()
    print("elapsed time: ", endtime - starttime)