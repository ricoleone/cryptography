########################################################################################
# Name: Frequency Analysis .py
# Description: Cracks a substituion cipher text using frequency analysis.
#              Assumes the cipher text is compose of contiguous lowercase alpha characters 
########################################################################################
from collections import Counter
f = open('BlackHatChallenge_03.txt','r')
cipherText = f.read()
f.close()
print(cipherText)
secret_key = {}

def genDigrams(text):
  for i in range(len(text) - 2 + 1):
    yield text[i:i+2]
    
def genTrigrams(text):
  for i in range(len(text) - 3 + 1):
    yield text[i:i+3]
    
def subText(dict, text):
  copyOf = text
  for key in dict.keys():
    print('key = ', key, ' value = ', dict.get(key))
    copyOf = copyOf.replace(key, dict.get(key))
  return copyOf
  
#count the frequency of each single character
letters = Counter(cipherText)
#print(letters)

# assign the most frequent letter to E
first = letters.most_common(1)
print('most common letter ', first)
secret_key.update({first[0][0]:'E'})
print(secret_key)

digrams = Counter(genDigrams(cipherText))
#print(digrams)

# Determine if top 2 digrams are  TH or HE
top2 = digrams.most_common(2)
print('top2 digrams are ', top2)
# extract digrams from the top list which is tuples of digrams and frequencies
top2 = [x[0] for x in top2]
print('top2 digrams are ', top2)
#look for HE first, if the second letter of the digraph is same as key for E then we know we have HE
tmp_dict = {}

#there is only one key at this point
for key in secret_key.keys():
  if secret_key.get(key) == 'E':
    if top2[0][1] == key:
      tmp_dict.update({top2[0][0]:'H'})
      if(top2[1][1] == top2[0][0]):
        tmp_dict.update({top2[1][0]:'T'})
    else:
      if top2[1][1] == key:
        tmp_dict.update({top2[1][0]:'H'})
      if(top2[1][1] == top2[0][0]):
        tmp_dict.update({top2[0][0]:'T'})
      
      
secret_key.update(tmp_dict)
tmp_dict.clear()

trigrams = Counter(genTrigrams(cipherText))
top3 = trigrams.most_common(3)
print(top3)
top3 = [x[0] for x in top3]
#cheating for now
secret_key.update({'e':'T'})
print('top3 Trigrams are ', top3)

print("secret key = ", secret_key)
print(cipherText,'\n\n')

print( subText(secret_key, cipherText) )

