#Linear congruential random number generator, similar to gcc
# R(i) = a * R(i-1) + c mod machine

def ranNumGen(R0, iter = 1):
    a = 1103515245
    c = 12345
    m = 2**31

    vals = [R0]
    for i in range(5):
        vals.append((a*vals[-1] + c) %m )
    return vals

print(ranNumGen(3,5))
print(pow(7,9,11))

