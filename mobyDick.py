import urllib3

http = urllib3.PoolManager()
response = http.request('GET', 'https://vip.udel.edu/crypto/mobydick.txt')

mobytext = response.data.decode('UTF-8')
print('Mobytext ', len(mobytext), mobytext[17], )

onlyletters = ''.join(filter(lambda x: x.isalpha(), mobytext))

loweronly = onlyletters.upper()

f = open("MOBYDICK.txt", 'w')
f.write(loweronly)
f.close()
loweronly = onlyletters.lower()
print("onlyletters lenght = ", len(loweronly))
frequency = {}
for ascii in range(ord('a'), ord('a')+26):
    frequency[chr(ascii)] = float(loweronly.count(chr(ascii)))/len(loweronly)

sum_freqs_squared = 0.0
for ltr in frequency:
    sum_freqs_squared += frequency[ltr]*frequency[ltr]

print ("Should be near .065 if plain: " + str(sum_freqs_squared))