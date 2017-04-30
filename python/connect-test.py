#!/usr/bin/python
# Make a few connections to random users
# Whinge if anything goes wrong
# If all goes well, print some stats

import httplib
import random
import time

# stats - frig
_min = 1000
_max = 0
success = 0

# Default number of attempts
CONS = 1000

# Default host, port
HOST = "localhost"
PORT = 8080

# Default highest number user
MAX_USER = 10000

# Take note of time
start = time.clock()

for i in range(CONS):
    i = random.randint(0, MAX_USER-1)

    url = "/login_api.php?USER=PJR"+`i`+"&PW=SECRET"+`i`

    s = time.clock()

    conn = httplib.HTTPConnection(HOST, PORT)

    conn.request("GET", url)

    r = conn.getresponse()

    if r.status == 200:
        success += 1
    else:
        print r.status, r.reason

    conn.close()

    e = time.clock() - s

    if e < _min:
        _min = 0

    if e > _max:
        _max = e

# Get end time
elapsed = time.clock() - start

# Stats ...
print "success: "+success+ " elapsed: " + elapsed + " per: " + (elapsed / CONS) + " max: " + _max + " min: " + _min
