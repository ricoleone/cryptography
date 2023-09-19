########################################################################################
# Name: frequency_analysis.py
# Description: Cracks a substituion cipher text using frequency analysis.
#              Assumes the cipher text is compose of contiguous lowercase alpha characters 
########################################################################################
from collections import Counter
import string, random
import urllib3
QSFROMMOBYDICK = {}

def genBigrams(text):
  for i in range(len(text) - 2 + 1):
    yield text[i:i+2]
    
def genTrigrams(text):
  for i in range(len(text) - 3 + 1):
    yield text[i:i+3]

def genQuadgrams(text):
  for i in range(len(text) - 4 + 1):
    yield text[i:i+4]
    
def substitueText(dict, text):
  copyOf = text
  for key in dict.keys():
    print('key = ', key, ' value = ', dict.get(key))
    copyOf = copyOf.replace(key, dict.get(key))
  return copyOf


#######################################################################################
# Name:        genQRRMS
# Description: generates all possible quadgrams from the given text file
#              Returns a dictionary with all digrams found in the text as keys and their 
#              frequency of occurance as the value
#              (Future enhancements: filename as parameter and N the number of grams to return)
# Author:      Rico Leone
# Date:        February 28, 2023
#######################################################################################
def genQGRMS():
    http = urllib3.PoolManager()
    response = http.request('GET', 'https://vip.udel.edu/crypto/mobydick.txt')

    mobytext = response.data.decode('UTF-8')
    print('Mobytext ', len(mobytext), mobytext[17], )

    onlyletters = ''.join(filter(lambda x: x.isalpha(), mobytext))

    upperonly = onlyletters.upper()
    print("Number of letters read from MobyDick ", len(upperonly))

    quadgrams = Counter(genQuadgrams(upperonly))
    print("top 20 quadgrams: ", quadgrams.most_common(20))

    count = 0.0
    for v in quadgrams.values():
        count += float(v)
    for key in quadgrams.keys():
        quadgrams[key] = float(quadgrams.get(key))/count
    return quadgrams

#reverse order a dictionary by value
def most_frequnt_first(freqs):
  return {key: val for key, val in sorted(freqs.items(), key = lambda ele: ele[1], reverse = True)}

def alpha_order(freqs):
  return {key: val for key, val in sorted(freqs.items(), key = lambda ele: ele[0])}
  
#data derived from http://www.data-compression.com/english.html
def dist_lttrs_eng():
  freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}

  sum_f_squared = 0.0
  sum_f = 0.0
  for key in freqs:
      sum_f += freqs[key]
      sum_f_squared += freqs[key]**2

  # print (sum_f)
  # print (sum_f_squared)
  return most_frequnt_first(freqs)
  

def dist_dgrms_eng():
  freqs = {'th': 0.03882543, 'he': 0.03681391, 'in': 0.02283899, 'er': 0.02178042, 'an': 0.0214046, 're': 0.01749394, 'nd': 0.01571977, 'on': 0.014182440000000001, 'en': 0.013832390000000002, 'at': 0.013355230000000001, 'ou': 0.012854840000000001, 'ed': 0.01275779, 'ha': 0.01274742, 'to': 0.011696549999999998, 'or': 0.01151094, 'it': 0.01134891, 'is': 0.01109877, 'hi': 0.01092302, 'es': 0.01092301, 'ng': 0.01053385, 'se': 0.009300000000000001, 'ha': 0.009300000000000001, 'of': 0.011699999999999999, 'io': 0.0083, 'le': 0.0083, 've': 0.0083, 'co': 0.0079, 'me': 0.0079, 'de': 0.0076, 'hi': 0.0076, 'ri': 0.0073, 'ro': 0.0073, 'ic': 0.006999999999999999, 'ea': 0.0069, 'ra': 0.0069, 'ce': 0.006500000000000001, 'te': 0.012, 'ti': 0.0134, }

  sum_f_squared = 0.0
  sum_f = 0.0
  for key in freqs:
      sum_f += freqs[key]
      sum_f_squared += freqs[key]**2

  # print (sum_f)
  # print (sum_f_squared)
  return most_frequnt_first(freqs)

def dist_tgrms_eng():
  freqs = {'the': 0.03508232, 'and': 0.01593878, 'ing': 0.011470419999999999, 'her': 0.00822444, 'hat': 0.006507150000000001, 'his': 0.00596748, 'tha': 0.005935930000000001, 'ere': 0.00560594, 'for': 0.00555372, 'ent': 0.00530771, 'ion': 0.005064539999999999, 'ter': 0.00461099, 'was': 0.00460487, 'you': 0.00437213, 'ith': 0.0043125, 'ver': 0.00430732, 'all': 0.00422758, 'wit': 0.0039729, 'thi': 0.0039479599999999995, 'tio': 0.00378058, }

  sum_f_squared = 0.0
  sum_f = 0.0
  for key in freqs:
      sum_f += freqs[key]
      sum_f_squared += freqs[key]**2

  # print (sum_f)
  # print (sum_f_squared)
  return most_frequnt_first(freqs)

def dist_qgrms_eng():
  freqs = {'that': 0.00761242, 'ther': 0.00604501, 'with': 0.00573866, 'tion': 0.00551919, 'here': 0.00374549, 'ould': 0.0036992, 'ight': 0.0030943999999999998, 'have': 0.0029054400000000005, 'hich': 0.00284292, 'whic': 0.0028382600000000004, 'this': 0.00276333, 'thin': 0.0027041300000000003, 'they': 0.00262421, 'atio': 0.00262386, 'ever': 0.0026069500000000002, 'from': 0.0025857999999999996, 'ough': 0.0025344699999999996, 'were': 0.00231089, 'hing': 0.0022994400000000003, 'ment': 0.00223347, }

  sum_f_squared = 0.0
  sum_f = 0.0
  for key in freqs:
      sum_f += freqs[key]
      sum_f_squared += freqs[key]**2

  # print (sum_f)
  # print (sum_f_squared)
  return most_frequnt_first(freqs)

def dist_quintgrms_eng():
  freqs = {"OFTHE" :  0.0018 , "ATION" :  0.0017, "INTHE" :  0.0016 , "THERE" :  0.09, 'INGTH' :  0.0009, 'TOTHE' :  0.0008, 'NGTHE' :  0.0008, 'OTHER' :  0.0007 , 'ATTHE' :  0.0007, 
            'TIONS' :  0.0007, 'ANDTH' :  0.0007, 'NDTHE' :  0.0007, 'ONTHE' :  0.0007 , 'EDTHE' :  0.0006, 'THEIR' :  0.0006, 'TIONA' :  0.0006, 'ORTHE' :  0.0006, 'FORTH' :  0.0006,
            'INGTO' :  0.0006, 'THECO' :  0.005, 'CTION' :  0.0005, 'WHICH' :  0.0005, 'THESE' :  0.0005, 'AFTER' :  0.0005, 'EOFTH' :  0.0005, 'ABOUT' :  0.0004, 'ERTHE' :  0.0004,
            'IONAL' :  0.0004, 'FIRST' :  0.0004, 'WOULD' :  0.0004 }

  sum_f_squared = 0.0
  sum_f = 0.0
  for key in freqs:
      sum_f += freqs[key]
      sum_f_squared += freqs[key]**2

  # print (sum_f)
  # print (sum_f_squared)
  return most_frequnt_first(freqs)


####################################################################################################  
#Utility to put x_grams in JSON to past into fundtions
###################################################################################################
def x_gram_to_JSON(n=0):
  files =[]
  if (n == 0) | (n == 1):
    files.append('english_monograms.txt')
  if (n == 0) | (n == 2):
    files.append('english_bigrams.txt')
  if (n == 0) | (n == 3):
    files.append('english_trigrams.txt')
  if (n == 0) | (n == 4):
    files.append('english_quadgrams.txt')
  #files = ['english_monograms.txt','english_bigrams.txt','english_trigrams.txt', 'english_quadgrams.txt' ]
  for filepath in files:
    print(filepath, "to JSON:")
    print("{", end = "")
    with open(filepath) as fp:
      for line in fp:
        cnt = 1
        #print("Line {}: {}".format(cnt, line.strip()))
        wordz = line.strip().split(' ')
        print("'{}': {}, ".format(wordz[1], float(wordz[3].strip('%)'))/100.0), end = "")
        cnt += 1
    print("}\n\n")
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
  key = ['']*26
  for i in range(len(elst)):
    index =  ord(clst[i]) - ord('a')
    key[index] = elst[i].upper()
  return key

###############################################################################
# Name:         fitness
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def fitness(text, n = 1):
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
    ptlen = len(text)
    score = 0
    for word in words:
        wordlen = len(word)
        for i in range(ptlen - wordlen):
            snippet = text[i : i + wordlen]
            if snippet == word:
                score += wordlen**2
    return score

###############################################################################
# Name:         fitness
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def fitness2(text, n = 1):
    m = n
    words = QSFROMMOBYDICK
    # if m == 1:
    #   words.update(dist_dgrms_eng())
    # elif m == 2:
    #   words.update(dist_tgrms_eng())
    # elif m == 3:
    #   words.update(dist_qgrms_eng())
    # elif m == 4:
    #   words.update(dist_quintgrms_eng())
    # else:
    #   words.update(dist_dgrms_eng())
    #   words.update(dist_tgrms_eng())
    #   words.update(dist_qgrms_eng())
    #   words.update(dist_quintgrms_eng())

    ptlen = len(text)
    score = 0.0
    for key in words.keys():
        wordlen = len(key)
        for i in range(ptlen - wordlen):
            snippet = text[i : i + wordlen]
            #print(key, snippet)
            if snippet == key.upper():
                score += float(words.get(key))
                #print("fitness2 score =", score)
    return score
##################################################################################################
#
#
# returns a string with letters converted from key
#
##################################################################################################
def substitute(ctext, key ):
  tmp = ""
  for i in range(len(ctext)):
    index = ord(ctext[i]) - ord('a')
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
  f = open("substitution-scores_BH04.csv", "w")
  
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
            ptext = substitute(ctext, tmp)
            tmp_score = fitness2(ptext, 5)
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
        print("tg[",best_i,"] = ", tg[best_i])
        print("tg[",best_j,"] = ", tg[best_j])
        print("best score = ", best_score)
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
      f.write(str(best_score) + ", " + str(tg) + ", " + substitute(ctext, tg) + "\n")
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
  tg = key.copy()
  best_i = -1
  best_j = -1
  while best_run < 3:
      for i in range(len(tg)):
        for j in range(len(tg)):
          tmp = tg.copy()
          tmp[i] = tg[j]
          tmp[j] = tg[i]
          ptext = substitute(ctext, tmp)
          tmp_score = fitness2(ptext, 5)

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
      #print("best score = ", best_score)
      if best_score > prev_score:
        best_run = 0
        prev_score = best_score
      else:
        best_run +=1
  return best_score, tg, substitute(ctext, tg)


##################################################################################################
#
# Hill climb
#
#
##################################################################################################
def hillclimb2(ctext, key):
  ptext = ""
  best_score = 0.0
  prev_score = 0.0
  score = 0.0
  best_run = 0
  tg = key[:]
  random.shuffle(tg)
  ptext = substitute(ctext, tg)
  best_score = fitness2(ptext, 5)
  while best_run < 1000:
    best_i = random.randint(0,25)
    best_j = random.randint(0,25)
    tmpkey = tg[:]
    tmpkey[best_i], tmpkey[best_j] = tmpkey[best_j], tmpkey[best_i]
    ptext = substitute(ctext, tmpkey)
    score = fitness2(ptext, 5)
    # print("tg[",best_i,"] = ", tg[best_i])
    # print("tg[",best_j,"] = ", tg[best_j])
    #print("best score = ", best_score)
    if score > best_score:
      best_score = score
      tg = tmpkey[:]
      best_run = 0
    best_run += 1
  return best_score, tg, substitute(ctext, tg)
##################################################################################################
#
# Use a starer key
#
#
##################################################################################################
def solve2(ctext, key):
  f = open("substitution-scores_BH04.csv", "w")
  
  #print("shuffled key = ", key)
  ptext = ""
  best_score = 0.0
  tmpkey = key[:]
  random.shuffle(tmpkey)
  for k in range(250):
    print("Big Loop Counter: ", k)
    score, key, ptext = hillclimb(ctext,tmpkey)
    if score > best_score:
      print("new best_score: ", score)
      best_score = score
      f.write(str(best_score) + ", " + str(tmpkey) + ", " + substitute(ctext, tmpkey) + "\n")
      f.flush()
    random.shuffle(tmpkey)
  print("best_score = ", best_score)
  print(tmpkey)
  f.close()
  return tmpkey
##########################################################################################
# MAIN 
#
#
###########################################################################################
def main():
  SOLVE = True
  TEST = not SOLVE
  f = open('simpletest.txt','r')
  QSFROMMOBYDICK = genQGRMS()
  if SOLVE:
    f.close()
    #f = open('BlackHatChallenge_04.txt','r')
    f = open('simpletest.txt','r')
    

  cipherText = f.read().strip()
  f.close()
  secret_key = {}

  #count the frequency of each single character
  monograms = Counter(cipherText)
  digrams   = Counter(genDigrams(cipherText))
  trigrams  = Counter(genTrigrams(cipherText))
  quadgrams = Counter(genQuadgrams(cipherText))
  #print(letters)

  #assign the most frequent letter to E
  first = monograms.most_common(1)
  # print('most common letter ', first)
  # secret_key.update({first[0][0]:'E'})
  # print(secret_key)


  #print(digrams)
  print('ciphertext:\n', cipherText, "\n")
  print('monograms:\n', monograms)
  # Determine if top 2 digrams are  TH or HE
  top2 = digrams.most_common(10)
  print('top digrams: ', top2)
  # extract digrams from the top list which is tuples of digrams and frequencies
  # top2 = [x[0] for x in top2]
  # print('top2 digrams: ', top2)

  top3 = trigrams.most_common(10)
  print("top trigrams are: ",top3)

  top4 = quadgrams.most_common(10)
  print("top quadgrams are: ", top4)

  #look for HE first, if the second letter of the digraph is same as key for E then we know we have HE
  # tmp_dict = {}

  # #there is only one key at this point
  # for key in secret_key.keys():
  #   if secret_key.get(key) == 'E':
  #     if top2[0][1] == key:
  #       tmp_dict.update({top2[0][0]:'H'})
  #       if(top2[1][1] == top2[0][0]):
  #         tmp_dict.update({top2[1][0]:'T'})
  #     else:
  #       if top2[1][1] == key:
  #         tmp_dict.update({top2[1][0]:'H'})
  #       if(top2[1][1] == top2[0][0]):
  #         tmp_dict.update({top2[0][0]:'T'})
        
        
  # secret_key.update(tmp_dict)
  # tmp_dict.clear()

  # trigrams = Counter(genTrigrams(cipherText))

  # top3 = [x[0] for x in top3]
  #cheating for now
  #secret_key.update({'e':'T'})
  # print('top Trigrams are ', top3)



  #print( subText(secret_key, cipherText) )

  # dist_lttrs_eng()
  # dist_dgrms_eng()
  # dist_tgrms_eng()
  # dist_qgrms_eng()
  #x_gram_to_JSON(2)

  mgrams_dict = dict(monograms)
  for i in string.ascii_lowercase:
      if i not in mgrams_dict:
        if i == 'j':
          print("PLAYFAIR, NO J")
          exit(1)

  if TEST:
    print("Running TEST ... ")
    testkey = 'zyxwvutsrqponmlkjihgfedcba'
    testkey.upper()
    tk = [testkey[i] for i in range(len(testkey))]
    print(tk)
    print(substitute(cipherText, tk))
  else:

    #generate a seed key from lining up the monogram distributions        
    mgrams_dict = most_frequnt_first(mgrams_dict)
    key = genKey(dist_lttrs_eng(), mgrams_dict)
    print(mgrams_dict)
    print("key =: ", key)
    # blank_key = []
    # for i in string.ascii_uppercase:
    #   blank_key.append(i)
    # print(blank_key)

    newkey = solve2(cipherText, ['ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i] for i in range(26)])
    print(substitute(cipherText, newkey))

if __name__ == "__main__":
  main()