import urllib3
from collections import Counter
import string, random

def genQuadgrams(text):
  for i in range(len(text) - 4 + 1):
    yield text[i:i+4]

def genQRMS():
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
# v = quadgrams.values()
# print("v0 = ", v[0], "v1 = ", v[1], "v2 = ", v[2])
# frequency = {}
# for ascii in range(ord('a'), ord('a')+26):
#     frequency[chr(ascii)] = float(loweronly.count(chr(ascii)))/len(loweronly)

# sum_freqs_squared = 0.0
# for ltr in frequency:
#     sum_freqs_squared += frequency[ltr]*frequency[ltr]

# print ("Should be near .065 if plain: " + str(sum_freqs_squared))