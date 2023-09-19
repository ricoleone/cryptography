########################################################################################
# Name:        crack_playfair.py
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
##################################################################################
# playfair_box_shift
# Author: Prfo Andy Noviac Universtity of Delaware
#
##################################################################################
def playfair_box_shift(i1, i2):
    r1 = int(i1/5)
    r2 = int(i2/5)
    c1 = i1 % 5
    c2 = i2 % 5
    out_r1 = r1
    out_c1 = c2
    out_r2 = r2
    out_c2 = c1
    if r1 == r2:
        out_c1 = (c1 + 1) % 5
        out_c2 = (c2 + 1) % 5
    elif c1 == c2:
        out_r1 = (r1 + 1) % 5
        out_r2 = (r2 + 1) % 5
    return out_r1*5 + out_c1, out_r2*5 + out_c2
##################################################################################
# playfair_enc
# Author: Prfo Andy Noviac Universtity of Delaware
#
##################################################################################
def playfair_enc(plain):
    #print("plaint text length = ", len(plain))
    words = list("this is ten random words needed to start this function".split())
    #print(words)
    random.shuffle(words)
    seed = "".join(words[:10]).replace('j','i')
    #print("seed = ", seed)
    alpha = 'abcdefghiklmnopqrstuvwxyz'
    suffix = "".join( sorted( list( set(alpha) - set(seed) ) ) )
    seed_set = set()
    prefix = ""
    for letter in seed:
        if not letter in seed_set:
            seed_set.add(letter)
            prefix += letter
    key = prefix + suffix
    #print("Key = ", key, " Lengnth = ", len(key))
    secret = ""
    for i in range(0,len(plain),2):
        chr1 = plain[i]
        chr2 = plain[i+1]
        if chr1 == chr2:
            chr2 = 'X'
        i1 = key.find(chr1.lower())
        i2 = key.find(chr2.lower())
        ci1, ci2 = playfair_box_shift(i1, i2)
        print(ci1, ", ", ci2)
        secret += key[ci1] + key[ci2]
    return secret, key

##################################################################################
# playfair_box_unshift
# Author: Rico Leone (Modified code from Prof. Andy Novocin)
#
##################################################################################
def playfair_box_unshift(i1, i2):
    r1 = int(i1/5)
    r2 = int(i2/5)
    c1 = i1 % 5
    c2 = i2 % 5
    out_r1 = r1
    out_c1 = c2
    out_r2 = r2
    out_c2 = c1
    if r1 == r2:
        out_c1 = (c1 + 4) % 5
        out_c2 = (c2 + 4) % 5
    elif c1 == c2:
        out_r1 = (r1 + 4) % 5
        out_r2 = (r2 + 4) % 5
    return out_r1*5 + out_c1, out_r2*5 + out_c2
##################################################################################
# dcrypt
# Author: Rico Leone (Modified code from Prof. Andy Novocin)
#
##################################################################################
def decrypt(ctext, key):
    ptext = ""
    for i in range(0,len(ctext),2):
        chr1 = ctext[i]
        chr2 = ctext[i+1]
        i1 = key.index(chr1.lower())
        i2 = key.index(chr2.lower())
        ci1, ci2 = playfair_box_unshift(i1, i2)
        ptext += key[ci1] + key[ci2]
    return ptext.upper()

##################################################################################
# Name:  dcrypt2
# Description: Same as encrypt but takes a key as a list object
# Author: Rico Leone (Modified code from Prof. Andy Novocin)
# 
##################################################################################
def decrypt2(ctext, key):
    ptext = ""
    for i in range(0,len(ctext),2):
        chr1 = ctext[i]
        chr2 = ctext[i+1]
        i1 = key.index(chr1.lower())
        i2 = key.index(chr2.lower())
        ci1, ci2 = playfair_box_unshift(i1, i2)
        ptext += key[ci1] + key[ci2]
    return ptext
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

###############################################################################
# Name:         fitness2
# Description: (from Prof. Andy Novocin UDEL Applied Cryptography)
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

################################################################################################
#
# 
################################################################################################
def hillclimb3(ctext, key):
  keylen = len(key)
  tg = key[:]
  random.shuffle(tg)
  ptext = decrypt(ctext, tg)
  best_score = fitness2(ptext,2)
  best_run = 0
  starttime = time.time()
  # optimal number of swaps is between 10**3 and 10**4
  swaps = 1250
  while best_run < swaps:
    best_i = random.randint(0,keylen - 1)
    best_j = random.randint(0,keylen - 1)
    tmpkey = tg[:]
    tmpkey[best_i], tmpkey[best_j] = tmpkey[best_j], tmpkey[best_i]
    ptext = decrypt(ctext, tmpkey)
    score = fitness2(ptext,2)
    # print(ptext)
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
  f = open("playfair-scores_BH05.csv", "w")
  #print("shuffled key = ", key)
  ptext = ""
  best_score = -9999999999
  prev_score = -9999999999
  score = 0.0
  tg = key[:]
  rnd = 1
  #print("ciphertext:",ctext)
  #optimum number of trials is between 40 and 80
  trials = 5000
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
##################################################################################
# main
# Author: Rico Leone 
#
##################################################################################
def main():

    SOLVE = True
    TEST = not SOLVE
    if SOLVE:
        global BGRAMS
        global TGRAMS
        global QGRAMS
        global SUM
        global MAX
        book = "MOBYDICK.txt"
        f = open('BlackHatChallenge_05.txt','r')
        SUM, MAX, QGRAMS = genGRMS(book, 4)
        ciphertext = f.read().strip()
        f.close()
        key = list('zyxwvutsrqponmlkihgfedcba')
        newkey = solve2(ciphertext, key)
        print(decrypt(ciphertext, newkey))

    else:    
        message = "thereisatreegrowinginthebackyardwithbigredleaves"
        ctext   = "QMGINEQYODKUGHGVUBOEEUQMHIYBSCLBBZDNQHREIGRFHPUGXY"
        ctext   = ctext.lower()
        ciphertext, key = playfair_enc(message)
        ptext   = decrypt(ciphertext, key)
        print("Message: ", message)
        print("Cihpher Text: ", ciphertext)
        print("Key: ", key)
        print("Plain Text: ", ptext)
if __name__ == "__main__":
    main()    