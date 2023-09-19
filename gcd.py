def gcd(a,b):
    print(a, ", ", b)
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

print("gcd(56,42) = ",gcd(56,42))
print("gcd(8,13) = ",gcd(8,13))
print("gcd(1071,462) = ",gcd(1071,462))