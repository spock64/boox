#!/usr/bin/python
# PJR-A 170501
# Make a few connections to random users
# Whinge if anything goes wrong
# If all goes well, print some stats
# It's configurable ...

import httplib
import random
import time
import getopt, sys

OPT_STR = "h:p:u:c:vx"
OPT_STR_EXT = ["host=", "port=", "user=", "connections=", "verbose","help"]

# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# Params ...

# Default number of attempts
CONS = 200

# Default host, port
HOST = "localhost"
PORT = 8080

# Default highest number user id
MAX_USER = 10000

# RT Flags
VERBOSE = False

# -----------------------------------------------------------------------------
def usage():
    print "**** PJR-A Simple Login performance evaluation"
    print "**** Params:"
    print "\t-h|--host hostname"
    print "\t\tHostname of API server"
    print "\t-p|--port port"
    print "\t\tPort number of API server"
    print "\t-u|--user max-user-id"
    print "\t\tMaximum User ID to probe"
    print "\t-c|--connections total-connections"
    print "\t\tTotal number of connections required"
    print "\t-v"
    print "\t\tVerbose mode"
    print "\t-x"
    print "\t\tValidate parameters and exit"

# -----------------------------------------------------------------------------
def process_params():
    # Process command line arguments
    global VERBOSE, HOST, PORT, MAX_USER, CONS

    EXIT_POST_PARAMS = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], OPT_STR, OPT_STR_EXT)
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-v","--verbose"):
            VERBOSE = True
        elif o == "--help":
            usage()
            sys.exit()
        elif o in ("-h", "--host"):
            HOST = a
        elif o in ("-p", "--port"):
            PORT = int(a)
        elif o in ("-u", "--user"):
            MAX_USER = int(a)
        elif o in ("-c", "--connections"):
            CONS = int(a)
        elif o in ("-x"):
            EXIT_POST_PARAMS = True
        else:
            assert False, "unhandled option"

    if VERBOSE:
        print "Host:port "+HOST+":"+`PORT`+" Max UID "+`MAX_USER`+" Connections "+`CONS`

    if EXIT_POST_PARAMS:
        print "Exiting as requested"
        sys.exit()

# -----------------------------------------------------------------------------
def run_test():

    global VERBOSE, HOST, PORT, MAX_USER, CONS

    # stats - frig
    _min = 1000
    _max = 0
    success = 0
    con_fails = 0
    req_fails = 0

    # Take note of time
    start = time.time()

    for j in range(CONS):
        i = random.randint(0, MAX_USER-1)

        url = "/login_api_ext.php?USER=PJR"+`i`+"&PW=SECRET"+`i`

        s = time.time()

        try:
            conn = httplib.HTTPConnection(HOST, PORT)
        except:
            # connection failed
            con_fails += 1

            if j == 0:
                # Fail on first conn failure ...
                print "Failed to connect"
                sys.exit(1)
            else:
                continue

        try:
            conn.request("GET", url)
        except:
            req_fails += 1

            if j == 0:
                print "Failed to hit API or connect"
                sys.exit(1)
            else:
                continue

        r = conn.getresponse()

        if r.status == 200:
            success += 1
        else:
            print r.status, r.reason

        conn.close()

        e = time.time() - s

        if e < _min:
            _min = e

        if e > _max:
            _max = e

    # Get end time
    elapsed = time.time() - start

    # Stats ...
    print "success: "+`success`+ " elapsed: " + `elapsed` + " /sec:" + `(CONS/elapsed)` + " per: " + `(elapsed / CONS)` + " max: " + `_max` + " min: " + `_min`
    if success != CONS:
        print "failed connections "+`con_fails`+" request fails "+`req_fails`

# -----------------------------------------------------------------------------
# Will be expanded to add multiprocess working
def main():

    global VERBOSE, HOST, PORT, MAX_USER, CONS

    process_params()

    # for now ...
    print "Connect test calling login_api_ext"
    run_test()

# -----------------------------------------------------------------------------
# Entrypoint
if __name__ == '__main__':
    main()
