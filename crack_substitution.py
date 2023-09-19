########################################################################################
# Name:        crack_substitution.py
# Description: Cracks a substituion cipher text using frequency analysis.
#              Assumes the cipher text is compose of contiguous lowercase alpha characters 
# Author:      Rico Leone
# Date:        February 27, 2023
########################################################################################
from collections import Counter
import collections
import string, random
import itertools
import urllib3, time
import frequency_analysis as fa

BGRAMS = {}
TGRAMS = {}
QGRAMS = {}
SUM    = 0.0
MAX    = 0.0

#######################################################################################
# Name:        genRRMS
# Description: generates all possible quadgrams from the given text file
#              Returns a dictionary with all digrams found in the text as keys and their 
#              frequency of occurance as the value
#              (Future enhancements: filename as parameter and N the number of grams to return)
# Input:       enter the text file, type of Ngram to produce 2 for BIgrams, 3 for TRIgrams, 
#              and 4 for QUADgrams, the number of Ngrams to output, where the default is all found
# Author:      Rico Leone
# Date:        February 28, 2023
#######################################################################################
def genGRMS(fname, g=2, n=0):
    
    f = open(fname, 'r')
    mobytext = f.read()
    onlyletters = ''.join(filter(lambda x: x.isalpha(), mobytext))
    

    upperonly = onlyletters.upper()
    print("Number of letters read from ",fname, ": ", len(upperonly))
    
    ngrams = {}

    if g == 2:
      ngrams = Counter(fa.genBigrams(upperonly))
    elif g == 3:
      ngrams = Counter(fa.genTrigrams(upperonly))
    elif g == 4:
      ngrams = Counter(fa.genQuadgrams(upperonly))

    sum = 0.0
    for v in ngrams.values():
        sum += float(v)
   
    for key in ngrams.keys():
        ngrams[key] = float(ngrams.get(key))/sum
    
    #This will be the penalty for an ngram in the calculated plaintext not being in the ngram dictionary
    max = ngrams.most_common()[0][1]

    ngrams = fa.alpha_order(ngrams)
    if n > 0:
      ngrams = dict(itertools.islice(ngrams.items(), n))
    print(fname, " NGRAMS RETURNED = ", len(ngrams), " ", g, "-grams")
    return sum, max, ngrams


###################################################################################################
#
#
#
#
##################################################################################################
def genKey(eng,ct):
  elst = list(eng.keys())
  clst = list(ct.keys())
  print("elst = " , elst)
  print("clst = ", clst)

  if len(clst) != len(elst):
    print("genKey: list not equal lenght")
    exit(0)
  
  key = ['']*26
  for i in range(len(elst)):
    index =  ord(elst[i]) - ord('a')
    key[index] = clst[i].upper()
  return key

###############################################################################
# Name:         fitness
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def fitness(ctext, n = 1):
    words = []
    dgrms  = ["TH", "HE", "IN", "ER", "AN", "RE", "ND", "HA", "TO", "IT", "ON", "EN", "AT", "OU", "HA", "OR", "IS", "ES", "NG", "EE", "TT", "SS", "OA"]
    tgrms   = ["THE", "MAN", "MEN", "AND", "ING", "ENT", "HIS", "HER", "YOU", "WAS""FOR", "ONE", "THA", "ERE", "ION", "TER", "ITH", "VER", "ALL" "WIT", "THI", "TIO" ]
    qgrms = ["TION", "SION", "THAT", "WITH","THIS", "FROM", "HAVE", "THEY", "WERE", "BEEN",  "WERE", "MENT", "ATIO", "THEN", "NEVER", "ALWAYS", "SOME", "LIKE", "MOST", "KNOW", "HERE", "OUGH", "WERE", "OULD"]
    if n == 3:
      words = dgrms
    elif n == 2:
      words = tgrms
    elif n == 1:
      words = qgrms
    else:
      words += dgrms
      words += tgrms
      words += qgrms
    # words = ["ONE", "TION", "SION", "THAT", "WITH","THIS", "FROM", "HAVE", "THEY", "WERE", "BEEN",  "WERE", "MENT"
    # "ATIO", "THEN", "NEVER", "ALWAYS", "SOME", "LIKE", "MOST", "KNOW", "HERE"]
    ctlen = len(ctext)
    score = 0
    wordlen = len(next(iter(words)))
    for i in range(ctlen - wordlen + 1):
      if ctext[i : i + wordlen] in words:
        score += words.get( ctext[i : i + wordlen] )
    return score

###############################################################################
# Name:         fitness2
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def fitness2(ctext, n=0):
    
    words = {}
    #print("SIZE OF WORDS ", len(words))
    if n == 0:
      words.update(BGRAMS)
    elif n == 1:
      words.update(TGRAMS)
    elif n == 2:
      words.update(QGRAMS)
    else:
      words.update(BGRAMS)
      words.update(TGRAMS)
      words.update(QGRAMS)

    ctlen = len(ctext)
    score = 0.0
    penalty = MAX
    wordlen = len(next(iter(words)))

    for i in range(ctlen - wordlen + 1):
      if ctext[i : i + wordlen] in words:
        score += words.get( ctext[i : i + wordlen] )
      else:
        #penalty for an ngram not appearing in the dictionary of ngrams (in otherwords, nonsense)
        score -= penalty

    return score
###############################################################################
# Name:         fitness
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def fitness3(text, n=0):
  freqs = {'a': 0.080642499002080981, 'b': 0.015373768624831691,'c': 0.026892340312538593, 'd': 0.043286671390026357, 'e': 0.12886234260657689, 'f': 0.024484713711692099, 'g': 0.019625534749730816, 'h': 0.060987267963718068, 'i': 0.06905550211598431, 'j': 0.0011176940633901926, 'k': 0.0062521823678781188, 'l': 0.041016761327711163, 'm': 0.025009719347800208, 'n': 0.069849754102356679, 'o': 0.073783151266212627,  'p': 0.017031440203182008, 'q': 0.0010648594165322703, 'r': 0.06156572691936394, 's': 0.063817324270355996, 't': 0.090246649949305979, 'u': 0.027856851020401599, 'v': 0.010257964235274787, 'w': 0.021192261444145363, 'x': 0.0016941732664605912, 'y': 0.01806326249861108,  'z': 0.0009695838238376564}
  ptext = text.lower()
  alpha_counts = []
  #print(ptext)
  alphas   = collections.Counter(ptext)
  #print(alphas)
  #insert 0 counts for alpha char not found in the text
  for i in string.ascii_lowercase:
    if i not in alphas:
      alphas.update({i : 0})
  tmpkeys = list(alphas.keys())
  tmpkeys.sort()
  alphasorted = {i: alphas[i] for i in tmpkeys}
  #print(alphasorted) 
  alpha_arr = [(alphas.get(c)) for c in string.ascii_lowercase]
  #print(alpha_arr)
  score = 0.0
  highscore = -999.99
  best_shift = 0
  for i in range(26):
    score = 0.0
    for c in string.ascii_lowercase:
      indx = (ord(c) - ord('a') + i) % 26
      score += freqs.get(c) * alpha_arr[indx]

  return score
##################################################################################################
#
#
# returns a string with letters converted from key
#
##################################################################################################
def encrypt(plaintext, key):
    # letters = range(26)
    # random.shuffle(letters)
    cipher = plaintext
    for i in range(len(key)):
        #pt = chr(65+i)
        cipher = cipher.replace(key[i], chr(ord('a') + i ))
    return cipher
##################################################################################################
#
#
# returns a string with letters converted from key
#
##################################################################################################
def decrypt(ctext, key ):
  tmp = ""
  tmpct = ctext.lower()
  for i in range(len(tmpct)):
    index = ord(tmpct[i]) - ord('a')
    tmp += key[index]
  #print(tmp)
  return tmp
##################################################################################################
#
# Use a starer key
#
#
##################################################################################################
def solve(ctext, key):
  f = open("substitution-scores_BH03.csv", "w")
  
  #print("shuffled key = ", key)
  ptext = ""
  best_score = 0.0
  prev_score = 0.0
  best_run = 0
  super_score = 0.0
  super_key = []
  tg = key.copy()
  print(tg)
  best_i = 0
  best_j = 0
  count = 0
  for k in range(3):
    print("Big Loop Counter: ", k)
    random.shuffle(tg)
    while best_run < 3:
        for i in range(len(tg)):
          for j in range(len(tg)):
            tmp = tg.copy()
            tmp[i] = tg[j]
            tmp[j] = tg[i]
            ptext = decrypt(ctext, tmp)
            tmp_score = fitness2(ptext, 3)
          # print("tmp_score = ", tmp_score)
          #print("tmp = ", tmp)
          if tmp_score > best_score:
            best_i = i
            best_j = j
            best_score = tmp_score
        # temp = tg[best_i]
        # tg[best_i] = tg[best_j]
        # tg[best_j] = temp
        tg[best_i], tg[best_j] = tg[best_j], tg[best_i]
        # print("tg[",best_i,"] = ", tg[best_i])
        # print("tg[",best_j,"] = ", tg[best_j])
        # print("best score = ", best_score)
        if best_score > prev_score:
          best_run = 0
          prev_score = best_score
          #f.write(str(best_score) + ", " + str(tg) + ", " + solve(ctext, tg) + "\n")
        else:
          best_run +=1
    print("Best_run = ", best_run)
    best_run = 0
    if best_score > super_score:
      print("best_score > super_score")
      super_score = best_score
      super_key   = tg
      f.write(str(best_score) + ", " + str(tg) + ", " + decrypt(ctext, tg) + "\n")
      f.flush()
  print("super score = ", super_score)
  print("previous score = ", prev_score)
  print(super_key)
  f.close()
  return tg
##################################################################################################
#
# Hill climb
#
#
##################################################################################################
def hillclimb(ctext, key):
  ptext = ""
  best_score = 0.0
  prev_score = 0.0
  best_run = 0
  tg = key[:]
  best_i = -1
  best_j = -1
  ptext = decrypt(ctext, key)
  best_score = fitness(ptext,4)
  print("Kick off key is ", tg )
  print("Kick off score is ", best_score )
  starttime = time.time()
  while best_run < 3:
    print("Round-> ", best_run)
    for i in range(len(tg)):
      for j in range(len(tg)):
        tmp = tg[:]
        tmp[i], tmp[j] = tg[j], tg[i]
        ptext = decrypt(ctext, tmp)
        tmp_score = fitness(ptext, 4)
        if tmp_score > best_score:
          best_i = i
          best_j = j
          best_score = tmp_score
    if (best_i == -1) | (best_j == -1):
      best_i = random.randint(0,25)
      best_j = random.randint(0,25)
    tg[best_i], tg[best_j] = tg[best_j], tg[best_i]
    # print("tg[",best_i,"] = ", tg[best_i])
    # print("tg[",best_j,"] = ", tg[best_j])
    # print("best score = ", best_score)
    if best_score > prev_score:
      best_run = 0
      prev_score = best_score
    else:
      best_run +=1
  endtime = time.time()
  print("elapsed time: ", endtime - starttime)
  return prev_score, tg, decrypt(ctext, tg)


##################################################################################################
#
# Hill climb
#
#
##################################################################################################
def hillclimb2(ctext, key, filen):
  ptext = ""
  best_score = 0.0
  prev_score = -999999999
  score = 0.0
  tg = key[:]
  rnd = 1
  while rnd < 200:
    random.shuffle(tg)
    ptext = decrypt(ctext, tg)
    best_score = fitness2(ptext,2)
    #print("Round ... ", rnd)
    best_run = 0
    spice = 0
    starttime = time.time()
    while best_run < 1000:
      best_i = random.randint(0,25)
      best_j = random.randint(0,25)
      tmpkey = tg[:]
      tmpkey[best_i], tmpkey[best_j] = tmpkey[best_j], tmpkey[best_i]
      ptext = decrypt(ctext, tmpkey)
      score = fitness2(ptext, 2)
      # print("tg[",best_i,"] = ", tg[best_i])
      # print("tg[",best_j,"] = ", tg[best_j])
      #print("best score = ", best_score)
      if score > best_score:
        best_score = score
        tg = tmpkey[:]
        best_run = 0
        #spice = (spice + 1)%3
      best_run += 1
      
    endtime = time.time()
    print("Round .....", rnd)
    print("elapsed time: ", endtime - starttime)
    if best_score > prev_score:
      print("Round .....", rnd)
      print("New best_score: ", best_score)
      print("New best key: ", tg)
      print("Plaintext: ", ptext)
      prev_score = best_score
      filen.write(str(tg) + ", " + str(best_score) + ", " +  decrypt(ctext, tg) + "\n")
      filen.flush() 
    rnd +=1  
  return best_score, tg, decrypt(ctext, tg)

################################################################################################
#
# 
################################################################################################
def hillclimb3(ctext, key):
  tg = key[:]
  random.shuffle(tg)
  ptext = decrypt(ctext, tg)
  best_score = fitness2(ptext,3)
  best_run = 0
  starttime = time.time()
  # optimal number of swaps is between 10**3 and 10**4
  swaps = 1250
  while best_run < swaps:
    best_i = random.randint(0,25)
    best_j = random.randint(0,25)
    tmpkey = tg[:]
    tmpkey[best_i], tmpkey[best_j] = tmpkey[best_j], tmpkey[best_i]
    ptext = decrypt(ctext, tmpkey)
    score = fitness2(ptext,3)
    if score > best_score:
      best_score = score
      tg = tmpkey[:]
      best_run = 0
    best_run += 1
  endtime = time.time()
  print("elapsed time: ", endtime - starttime)
  return best_score, tg
##################################################################################################
#
# Use a starer key
#
#
##################################################################################################
def solve2(ctext, key):
  f = open("substitution-scores_BH03.csv", "w")
  #print("shuffled key = ", key)
  ptext = ""
  best_score = -9999999999
  prev_score = -9999999999
  score = 0.0
  tg = key[:]
  rnd = 1
  print("ciphertext:",ctext)
  #optimum number of trials is between 40 and 80
  trials = 50
  while rnd < trials :
    print("Round ", rnd)
    ptext = ""
    best_score, tmptg = hillclimb3(ctext,tg)
    if best_score > prev_score:
        print("Round .....", rnd)
        print("New best_score: ", best_score)
        print("New best key: ", tmptg)
        print("Plaintext: ", decrypt(ctext, tmptg))
        prev_score = best_score
        tg = tmptg
        f.write(str(tg) + ", " + str(best_score) + ", " +  decrypt(ctext, tg) + "\n")
        f.flush()
    rnd +=1    
  f.close()
  return tg
##########################################################################################
# MAIN 
#
#
###########################################################################################
def main():
  global BGRAMS
  global TGRAMS
  global QGRAMS
  global SUM
  global MAX
  SOLVE = True
  TEST = not SOLVE
  book = "MOBYDICK.txt"
  qfile = "quadgrams.txt"
  f = open('BlackHatChallenge_03.txt','r')
 
 
  if TEST:
    f.close()
    f = open('simpletest.txt','r')

  # BGRAMS = genGRMS(book, 2, 30)
  # TGRAMS = genGRMS(book, 3, 30)
  SUM, MAX, QGRAMS = genGRMS(book, 4)
  #SUM, QGRAMS = genQGRMS(qfile)
  
  cipherText = f.read().strip()
  f.close()
  
  #count the frequency of each single character
  monograms = Counter(cipherText)
  # digrams   = Counter(fa.genBigrams(cipherText))
  # trigrams  = Counter(fa.genTrigrams(cipherText))
  # quadgrams = Counter(fa.genQuadgrams(cipherText))

  #print(digrams)
  print('ciphertext:\n', cipherText, "\n")
  print('monograms:\n', monograms)
  

  mgrams_dict = dict(monograms)
  for i in string.ascii_lowercase:
      if i not in mgrams_dict:
        mgrams_dict.update({i : 0}) 
             

  if TEST:
    print("Running TEST ... ")
    testkey = 'zyxwvutsrqponmlkjihgfedcba'
    print("testkey: ", testkey)
    testkey = testkey.upper()
    tk = list(testkey)
    print(tk)
    Nkey = solve2(cipherText, tk)
    print(Nkey)
    if Nkey == tk:
      print("Test Converged")
    else:
      print("Test Failed to Converge. Try again!")
      print(decrypt(cipherText, Nkey))
  else:

    #generate a seed key from lining up letter frequency with monogram distributions        
    # mgrams_dict = fa.most_frequnt_first(mgrams_dict)
    # key = genKey(fa.dist_lttrs_eng(), mgrams_dict)
    # print(mgrams_dict)
    # print("key =: ", key, "length = ", len(key))
    # # blank_key = []
    # for i in string.ascii_uppercase:
    #   blank_key.append(i)
    # print(blank_key)

    #newkey = solve2(cipherText, ['ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i] for i in range(26)])
    key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    #random.shuffle(key)
    newkey = solve2(cipherText, key)
    print(decrypt(cipherText, newkey))
    
if __name__ == "__main__":
  main()