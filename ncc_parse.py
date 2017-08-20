#!/usr/bin/env python3

"""Module docstring.

Nutanix Cluster Check (NCC) log parser
usage: ncc_parse <logfile>
"""

import os
import sys
import getopt
import re

__version__ = '0.1'

def key_find_detail(logfile, key):
    """find the detailed information for a key in the logfile"""
    m = re.search('^Detailed information for %s\:(.*?)^(Refer.*?)(^Detailed information for |^\+[-]+)' % key, logfile, re.DOTALL|re.MULTILINE)
    print('NCC check:')
    print('Detailed information for %s:' % key)
    if m:
        print(m.group(1))
        print('Solution:\n%s' % m.group(2))
    else:
        print('Regexp no match for %s' % key)
    print('--------------------------------------------------------------------------------\n')

def log_search_no_pass(logfile):
    """search a log file for tests that didn't pass and return the keys"""
    prepend = ""
    keys = []
    for line in logfile.splitlines():
        line = line.rstrip('\n')
        # see if this is a test and get the status
        # join lines if the test result is on the next line
        if len(prepend):
            line = prepend + line
        if re.search('^(\/[\w\/]*)\s*$', line):
            prepend = line
            continue
        else:
            prepend = ""
        # check each test to see if it passed
        m = re.search('^(\/[\w\/]*)[\s\b]*\[\s*(\w+)\s*\]\s*$', line)
        if m and m.group(2) != "PASS":
            keys.append(os.path.basename(m.group(1)))
                
    return keys

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
    # process arguments
    for arg in args:
        if not os.path.exists(arg):
            print("%s not found" % arg)
            continue

        try:
            with open(arg, 'r') as filehandle:
                logfile = filehandle.read()
        except IOError:
            print("Could not read %s" % arg)
            sys.exit(3)

        nopass = log_search_no_pass(logfile)
        for key in nopass:
            #look for the output for a particular key
            key_find_detail(logfile, key)


if __name__ == '__main__':
    main()