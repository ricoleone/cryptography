#generate the sequence of numbers up to 23 raised to a power mod 23 for the first 22 outputs, show the distnct set to the right
import random
def GCD(a,b):
    if b == 0:
        return a
    else:
        return GCD(b, a%b)
    
def euler_phi(M):
    m = 0
    for i in range(M):
        if GCD(i,M) == 1:
            m +=1
    return m
def sub_group(k):
    sep = "\t"
    if k >= 10:
        sep += "\t"
    for i in range(1, k):
        Ggroup = [pow(i,j,k) for j in range(k)]
        Gset   = set(Ggroup)
        GSlen  = len(Gset)
        print( i, Ggroup , sep, Gset, GSlen )
        if i == 1:
            sep = "\t"
        

def main():
    p = 151
    q = 257
    n = p*q
    # sub_group(k)
    phi = euler_phi(n)
    print("p = ", p, ", q = ",q)
    print("phi(", n, ") = ", phi )
    if phi == (p-1)*(q-1):
        print("phi n == (p-1)*(q-1)")
        print(n ," - phi =", n - phi)
        print("p + q = ", p+q)
        d = random.randint(1, n -1)
        while GCD(d, n) != 1:
            d = random.randin(1, n -1)
        print("random int d = ", d)
        print("d**phi (mod n) = ", pow(d, phi, n))
if __name__ == "__main__":
    main()