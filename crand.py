import binascii

def crand(seed):
    r=[]
    r.append(seed)
    for i in range(30):
        r.append((16807*r[-1]) % 2147483647)
        if r[-1] < 0:
            r[-1] += 2147483647
    for i in range(31, 34):
        r.append(r[len(r)-31])
    for i in range(34, 344):
        r.append((r[len(r)-31] + r[len(r)-3]) % 2**32)
    while True:
        next = r[len(r)-31]+r[len(r)-3] % 2**32
        r.append(next)
        yield (next >> 1 if next < 2**32 else (next % 2**32) >> 1)

my_generator = crand(123)
for i in range(5):
    print(next(my_generator))

mygen = crand(1983)
firstfour = [next(mygen) for i in range(4)]
print(firstfour)

mygen = crand(1983)
plaintext = "andy rules!!"

ct = "".join([chr(ord(plainchr) ^ (next(mygen) % 256)) for plainchr in plaintext])
print('ct', ct)

# Decrypt: I have encoded a CTF FLAG using seed 54321. 
# The message is '5ecce596975db5e0c3c7516f05db6ffb43c4e055e6dd' (as hex of course). 
# Find the original.
mygen = crand(54321)
ct = b'5ecce596975db5e0c3c7516f05db6ffb43c4e055e6dd'
print(ct)
pt = "".join([chr(ord(plainchr) ^ (next(mygen) % 256)) for plainchr in ct])
# ctb = b''
# ctb += ct
print('pt', pt)