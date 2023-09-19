import urllib3
http = urllib3.PoolManager()
r = http.request('GET', 'http://crypto.prof.ninja/dictionary.txt')
file = open('dictionary.txt', 'w')
file.write(r.data.decode('utf-8'))
file.close()