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
import os
from multiprocessing import Pool, Process

OPT_STR = "h:p:u:c:t:vx"
OPT_STR_EXT = ["host=", "port=", "user=", "connections=", "threads=", "verbose", "help"]


# -------------------------------------------------------------------------
# Params ...

# Default number of attempts
CONS = 200

# Default host, port
HOST = "localhost"
PORT = 8080

# Default highest number user id
MAX_USER = 10000

# Number of processes to running
THREADS = 1

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
    print "\t\tTotal number of connections required PER THREAD"
    print "\t|--threads number-of-threads"
    print "\t\tNumber of threads to run"
    print "\t-v"
    print "\t\tVerbose mode"
    print "\t-x"
    print "\t\tValidate parameters and exit"

# -----------------------------------------------------------------------------
def process_params():
    # Process command line arguments
    global VERBOSE, HOST, PORT, MAX_USER, CONS, THREADS

    EXIT_POST_PARAMS = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], OPT_STR, OPT_STR_EXT)
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)

    # PJR - should validate the integer conversion ?
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
        elif o in ("-t", "--threads"):
            THREADS = int(a)
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
def process_info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

# -----------------------------------------------------------------------------
def run_test(name):

    global VERBOSE, HOST, PORT, MAX_USER, CONS

    process_info(name)

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

    global THREADS

    procs = []

    process_params()

    if THREADS > 1:

        print "Starting "+`THREADS`+" threads"

        for i in range(THREADS):
            n = "Thread "+`i`
            p = Process(target = run_test, args = (n,))
            procs.append(p)
            p.start()

        print "Waiting for threads to complete"

        for i in range(THREADS):
            procs[i].join()

        print "Done"

        if 0:

            print "Starting "+`THREADS`+" threads"

            p = Pool(THREADS)

            for i in range(THREADS):
                rc = p.apply_async(run_test, ("Thread "+`i`,))

            print "Waiting for threads to complete"
            p.close()
            p.join()

            print "*** All done ***"

    else:

        # just run one ...
        print "Connect test calling login_api_ext"
        run_test("Single thread")

# -----------------------------------------------------------------------------
# Entrypoint
if __name__ == '__main__':
    main()
