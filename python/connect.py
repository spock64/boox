#!/bin/python
# Makes a connection to a random user

import httplib
import random

# Default host
HOST = "127.0.0.1"

# Default highest number user
MAX_USER = 10000

i = random.randint(0, MAX_USER-1)

url = HOST+"/login_api.php?USER=PJR"+`i`+"PW=SECRET"+`i`

conn = httplib.HTTPSConnection(url)

conn.request("GET", url)

r1 = conn.getresponse()

print r1.status, r1.reason


print r1.read()



conn.close()
