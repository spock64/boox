#!/usr/bin/python

import pymysql
import random
from sets import Set

unum = 10000
cnum = 50
entnum = 20

print "*** Set up users, channels, entlements ... ***"

con = pymysql.connect(host='localhost',
        user='root',
        password='pjr9npassword',
        db='JTEST')

try:
    with con.cursor() as cur:
        for i in range(0,unum):
            # Create one ...
            s = "INSERT INTO `USERS` (`NAME`, `PW`) VALUES (%s, %s)"
            cur.execute(s, ('PJR'+`i`, 'SECRET'+`i`))

        con.commit()


    with con.cursor() as cur:
        print("*** TEST ***")
        # Read back ...
        s = "SELECT `ID`, `PW` FROM `USERS` WHERE `NAME`=%s"
        cur.execute(s, ('PJR1'))
        r = cur.fetchone()
        print(r)

finally:
    print("*** USER INSERTS DONE ***")

try:
    with con.cursor() as cur:
        for i in range(0,cnum):
            # Create one ...
            s = "INSERT INTO `CHANNELS` (`NAME`) VALUES (%s)"
            cur.execute(s, ('CHANNEL'+`i`))

        con.commit()


    with con.cursor() as cur:
        print("*** TEST ***")
        # Read back ...
        s = "SELECT `ID` FROM `CHANNELS` WHERE `NAME`=%s"
        cur.execute(s, ('CHANNEL1'))
        r = cur.fetchone()
        print(r)

finally:
    print("*** CHANNEL INSERTS DONE ***")

# Create user's entitlements to view channels
# For each customer, create nument entitlements from the channels

try:
    with con.cursor() as cur:

        percent = 0.0

        for i in range(1, unum + 1):
            channels = Set([])

            while len(channels) < entnum:
                # pick a random channel
                c = `random.randint(1, cnum)`
                if not c in channels:
                    channels.add(c)
            if (i % 1000) == 0:
                percent = i / unum
                print("*** "+`percent`+"%")
                print("*** User "+`i`+" Channels ",channels)

            for c in channels:
                s = "INSERT INTO `USERCHANNEL` (`USERID`, `CHANNELID`) VALUES (%s, %s)"
                cur.execute(s, (`i`, `c`))

            con.commit()

finally:
    print("*** Channel entitlements set up ***")

con.close()
print("*** SETUP DONE ***")
