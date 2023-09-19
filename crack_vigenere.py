import string, collections
#f = open('encrypted.txt','r')
#ct = f.read()
# words = [word.strip() for word in f]
#f.close()

# onlyletters = ''.join(filter(lambda x: x.isalpha(), words))
# loweronly = onlyletters.lower()
# # we know the key is length 10 so lets look at every 1oth character and cycle through the alphabet until we get the expected sum of the squares of frequncies for the 10 char key
# for i in range(10):
#   frequency = {}
#   for ascii in range(ord('a'), ord('a')+26):
#     frequency[chr(ascii)] = float(loweronly.count(chr(ascii)))/len(loweronly)


#From lecture
def shiftBy(ltr, shift):
   return chr(ord('a') + (ord(ltr) - ord('a') + shift) % 26)

def vig(text, key):
  result = ""
  for i in range(len(text)):
    result += shiftBy(text[i], key[i % len(key)])
  return result

def findkeylen(text):
  lengths = [(keylen, collections.Counter(text[::keylen])) for keylen in range(10,20)]
  
  for i in range(len(lengths)):
    print(lengths[i])

#shows the expected occurances of english letters in a file of size 
def expectedfrequency(size):
  freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
  #occurances = freqs = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
  counts = {}
  for key in freqs.keys():
    counts[key] = float(freqs.get(key))*size
  print(counts)

#method to find key length and determine if the file is vigenere ciphertext
def coincidences(ct):
  cn = []
  for i in range(1, len(ct)):
    sum = 0
    for j in range(len(ct) - i):
      if ct[j] == ct[j + i]:
        sum += 1
    #print(i, ", ", sum)
    cn.append((i, sum))
  return cn

# determines the value of the ith key position
# input is the block of ciphtertext for each element that was encoded witht the ith key element

def findShift(text, keylen):
  freqs = {'a': 0.080642499002080981, 'b': 0.015373768624831691,'c': 0.026892340312538593, 'd': 0.043286671390026357, 'e': 0.12886234260657689, 'f': 0.024484713711692099, 'g': 0.019625534749730816, 'h': 0.060987267963718068, 'i': 0.06905550211598431, 'j': 0.0011176940633901926, 'k': 0.0062521823678781188, 'l': 0.041016761327711163, 'm': 0.025009719347800208, 'n': 0.069849754102356679, 'o': 0.073783151266212627,  'p': 0.017031440203182008, 'q': 0.0010648594165322703, 'r': 0.06156572691936394, 's': 0.063817324270355996, 't': 0.090246649949305979, 'u': 0.027856851020401599, 'v': 0.010257964235274787, 'w': 0.021192261444145363, 'x': 0.0016941732664605912, 'y': 0.01806326249861108,  'z': 0.0009695838238376564}
  alpha_counts = []
  print(text)
  alphas   = collections.Counter(text)
  print(alphas)
  #insert 0 counts for alpha char not found in the text
  for i in string.ascii_lowercase:
    if i not in alphas:
      alphas.update({i : 0})
  tmpkeys = list(alphas.keys())
  tmpkeys.sort()
  alphasorted = {i: alphas[i] for i in tmpkeys}
  print(alphasorted) 
  alpha_arr = [(alphas.get(c)) for c in string.ascii_lowercase]
  print(alpha_arr)
  score = 0.0
  highscore = -999.99
  best_shift = 0
  for i in range(26):
    score = 0.0
    for c in string.ascii_lowercase:
      indx = (ord(c) - ord('a') + i) % 26
      score += freqs.get(c) * alpha_arr[indx]
    print(i ," score =", score)  
    if score > highscore:
      highscore = score
      best_shift = i
      print("best shift =", best_shift, ", highscore = ", highscore)
  print("best shift =", best_shift, ", highscore = ", highscore)
  return best_shift
  
##############################################################################
# Name:        solve
# Description: given ciptertext and an array of numbers representing the shift
#              value for each element in the key, returns a string of plaintext
# Usage: 
# Author:
# Date:
##############################################################################
def solve(raw, key):
  def shiftEnc(c, n):
    return chr(((ord(c) - ord('a') - n) % 26) + ord('a'))
  pt = "".join([shiftEnc(raw[i], key[i % len(key)]) for i in range(len(raw))])
  print("solve:")
  print(pt.upper())
# print(string.printable)
# m = list(map(ord, string.printable))
# print(m)
# foo = string.printable
# for char in foo:
#   print(ord(char))
#rotate 't' forward by 17,
# val = ord('t') - ord('a') #= 19
# val += 17           #shift by 17 alpha chars
# val %= 26                  #loops into the alphabet
# print("val =", val)
# lttr = chr(val + ord('a')) #maps back to the ascii value 'k'
# print("new letter = ", lttr)



# r = vig("aaaaaaaaaa", [0,1,2,3])
# print(r) 
def test():
  # f = open('BlackHatChallenge_04.txt','r')
  # ct = f.read()
  # # words = [word.strip() for word in f]
  # f.close()
  # f = open('plaintext.txt','r')
  # pt = f.read()
  # pt = pt.lower()
  # # words = [word.strip() for word in f]
  # f.close()
  # print("ciphertext:\n", ct)
  # findkeylen(ct)
  # print("someplaintext:\n", pt)
  # findkeylen(pt)
  # #print("\nThe expected occurances: \n", expectedfrequency(len(pt)))
  # #test string for coincidences is "vvhqwvvrmhusgjg" should get 4 as period between high number of occurances
  # cq = coincidences(ct)
  # for i in range(len(cq)):
  #   print(cq[i])
  # findShift(ct[12::13], 13)
  ct = "UNIBGFBQCSENAGHUGQTWFQMTHTYIPFENAGHUGQTTAODTQALQBBPMQWSZSQBFEUSPCGLRPFQZMUVQLEHOHYFPIENTJGSLQBHZUFJCZCFJGNYEUHAVQUVAOSIHMZAPZFBMOHAMBFOWUZEFQGAWSMFXECGVFBAMHAGKALPTOZXZPHAZPFSPMUTZUEQBUMLPFBROXMCRQQFREQTFFQCEUVQVQFTIBAMSFNTFRAAEPIF"
  ct = ct.lower()
  print(ct)
  cq2 = coincidences(ct)
  for i in range(len(cq2)):
    print(cq2[i])
  #key is mumbo -> 12,20,12,1,14
  key = []
  keylen = 5
  for i in range(keylen):
    key.append(findShift(ct[i::keylen], keylen))
  #findShift(foo[4::5], 5)
  #solve(foo, [12,20,12,1,14])
  solve(ct, key)
  
def main():
  f = open('BlackHatChallenge_04.txt','r')
  ct = f.read()
  #ct = [word.strip() for word in f]
  f.close()
  key =[]
  keylen = 13
  for i in range(keylen):
    key.append(findShift(ct[i::keylen], keylen))
  print("key = ", key)
  solve(ct, key)
  print("\nrunning test ....")
  test()
if __name__ == "__main__":
  main()