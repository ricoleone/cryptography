import collections
import matplotlib.pyplot as plt

f = open('BlackHatChallenge_05.txt', 'r')
ct = [word.strip() for word in f][0]

data = collections.Counter(ct)
sortedDict = {}
for key, value in data.items():
    sortedDict[key] = value

sortedDict = sorted(sortedDict.items(), key=lambda x:x[1], reverse=True)

data = dict(sortedDict)

x = list(data.keys())
print(x)
y = list(data.values())
print(y)

plt.bar(x,y)
plt.title("Blackhat Challenge 4 - letter frequency distribution")
plt.xlabel("letters")
plt.ylabel("frequency")
plt.savefig('bh4_frequency.png')
plt.show()