#!/usr/bin/python
# Makes a connection to a random user

import httplib
import random

# Default host
HOST = "localhost"

# Default highest number user
MAX_USER = 10000

i = random.randint(0, MAX_USER-1)

url = "/login_api.php?USER=PJR"+`i`+"PW=SECRET"+`i`

conn = httplib.HTTPSConnection(HOST)

conn.request("GET", url)

r1 = conn.getresponse()

print r1.status, r1.reason


print r1.read()



conn.close()
