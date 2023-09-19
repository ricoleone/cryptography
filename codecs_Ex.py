import codecs

m = "Hi there"

print(m, type(m))

hexstr = codecs.encode(m.encode(), 'hex')

print(hexstr, type(hexstr))

integer_m = int(hexstr, 16)

print(integer_m, type(integer_m))

back2hex = format(integer_m, 'x').encode()

print(back2hex, type(back2hex))

plaintext = codecs.decode(back2hex, 'hex').decode('utf-8')

print(plaintext, type(plaintext))
