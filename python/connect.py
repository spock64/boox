#!/usr/bin/python
# Makes a connection to a random user

import httplib
import random

# Default host, port
HOST = "localhost"
PORT = 8080

# Default highest number user
MAX_USER = 10000

i = random.randint(0, MAX_USER-1)

url = "/login_api.php?USER=PJR"+`i`+"&PW=SECRET"+`i`

conn = httplib.HTTPConnection(HOST, PORT)

conn.request("GET", url)

r = conn.getresponse()

print r.status, r.reason

print r.getheaders()
print r.read()
print r.version



conn.close()
