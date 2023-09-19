import random, time
from numpy import matrix
from datetime import datetime
###############################################################################
# hill_enc
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################


###############################################################################
# Name:         fitness
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def fitness(plaintext, words):
    ptlen = len(plaintext)
    score = 0
    for word in words:
        wordlen = len(word)
        for i in range(ptlen - wordlen):
            snippet = plaintext[i : i + wordlen]
            if snippet == word:
                score += wordlen**2
    return score

###############################################################################
# hill_enc
# Description: (from Andy Novocin UDEL Applied Cryptography)
#              takes plaintext and outputs ciphertext encrypted using
#              Hill 2x2 cipher
###############################################################################
def hill_enc(plain):
    found = False
    a=1
    b=1
    c=1
    d=1
    def c2i(character):
        return ord(character)-ord('A')
    def i2c(encoded):
        return chr(ord('a') + encoded)

    while not found:
        a,b,c,d = [random.randint(0,25) for i in range(4)]
        det = (a*d - b*c) % 26
        det2 = ((a-1)*d - b*(c-1)) % 26
        if (det % 2 != 0 )and (det % 13 != 0) and (det2 % 26 != 0):
            found = True
    secret = ''
    for i in range(0, len(plain), 2):
        i1 = c2i(plain[i])
        i2 = c2i(plain[i+1])
        c1 = (i1*a + i2*b) % 26
        c2 = (i1*c + i2*d) % 26
        secret += i2c(c1) + i2c(c2)
    return secret, [a,b,c,d]

####################################################################################
# Name: hil_dec
# Description:
#####################################################################################
def hill_dec(ciphertext, key):
    input = [] 
    [[key(i),key(i+1)] for i in range(0,4,2)]
    A = matrix (input)
    print(A)

####################################################################################
# Name: hill_brute
# Description:
#####################################################################################
def hill_brute(ctext, a, b, c, d):
    #helper function
    def c2ii(character):
        return ord(character) - ord('a')
    def i2cc(encoded):
        return chr(ord('A') + encoded)
    secret = ''
    for i in range(0, len(ctext), 2):
        i1 = c2ii(ctext[i])
        i2 = c2ii(ctext[i+1])
        c1 = (i1*a + i2*b) % 26
        c2 = (i1*c + i2*d) % 26
        secret += i2cc(c1) + i2cc(c2)
    return secret, [a,b,c,d]

####################################################################################
# Name: solve
# Description:
#####################################################################################
def sovle(ctext, filename):
    f = open("hill2x2-scores_BH01.csv", "w")
    #f.write(filename)
    f.write("\n")
    # f2 = open('top100.txt','r')
    # words = [word.strip().upper() for word in f2]
    # f2.close()
    
    words = ["BE", "TO", "OF","THE", "MAN", "MEN", "AND", "ING", "ENT", "ION", "HER", "HER",
    "FOR", "ONE", "SION", "TION", "THAT", "WITH","THIS", "FROM", "HAVE", "THEY", "WERE",
    "BEEN", "WERE", "THEN", "NEVER", "ALWAYS", "SOME", "LIKE"]

    if UNITTEST:
        words += ["BANANA", "CYPT", "HUMAN", "LIBERTY"]    
    print(words)
    pt  = ""
    key = []
    bestkey = []
    score = 0 
    highscore = 0
    solved = ""
    count = 0
    for a in range(26):
        for b in range(26):
            for c in range(26):
                for d in range(26):
                    pt, key = hill_brute(ctext, a, b, c, d)
                    score = fitness(pt, words)
                    count += 1
                    if score > 200:
                        if score > highscore:
                            highscore = score
                            bestkey = key
                            solved  = pt
                        f.write(str(score) + ", " + str(key) + ", " + pt + "\n")
                        #else:
                            #if (score == highscore) | (score > (highscore - 5)) and ((highscore - 5) > 0):
                                #f.write(str(score) + " " + str(key) + " " + "\n" + pt + "\n")

    print("count: ", count, "\nhigh score: ", highscore, "\nkey: ", bestkey)
    print(solved)
    return solved, bestkey
####################################################################################
# Name: test
# Description: run the encryption and decryption and compare results to the plaintext
#####################################################################################
SOLVE = True
UNITTEST  = not SOLVE

pt = "THISISSOMEPLAINTEXTUSEDTOTESTTHEDECRYPTIONFUNCTIONBANANALIBERTYHUMAN"
#pt = "MUBYAQIQGNAEWOSRZQJIRZQKCLIZAGSXCJAAQRRM"
ct =""
ck =[]
ct2 = ""
ck2 = []
filename = ""
print("test started at ", datetime.now().strftime('%A %d-%m-%Y, %H:%M:%S'))
if SOLVE:
    filename = 'BlackHatChallenge_01.txt'
    f = open(filename, 'r')
    ct = f.read()
    f.close()
    #ct = ct.upper()
    if len(ct) % 2 == 1:
        ct += 'x'
if UNITTEST:   
    filename = "local"
    #pt = "THISISSOMEPLAINTEXTUSEDTOTESTTHEDECRYPTIONFUNCTIONBANANA"
    #pt = "MUBYAQIQGNAEWOSRZQJIRZQKCLIZAGSXCJAAQRRM"
    ct, ck = hill_enc(pt)

starttime = time.time()
ct2, ck2 = sovle(ct, filename)
endtime = time.time()
print("elapsed time: ", endtime - starttime)
print("sample text = ", pt)
print("ciphertext  = ", ct)
print("plaintext   = ", ct2)
print("key         = ", ck)
print("key inv     = ", ck2)