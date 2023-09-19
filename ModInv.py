i = 0
found = False
while i < 30:
    prod = i * 16
    r = prod % 19
    print(i, ", ", r)
    # if r == 1:
    #     print(i, " product = ", prod)
    #     found = True
    i += 1