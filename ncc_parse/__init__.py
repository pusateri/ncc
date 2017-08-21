#!/usr/bin/env python3

"""Module docstring.

Nutanix Cluster Check (NCC) log parser
usage: ncc_parse [-c <case number>] [-f text|html] <logfile>
"""

import os
import sys
import getopt
import re

__version__ = '0.2'

def output_heading(fmt, level, value):
    if fmt == 'text':
        print('%s:' % value)
    elif fmt == 'html':
        print('<h%s>%s:</h%s>' % (level, value, level))

def output_paragraph(fmt, value):
    if fmt == 'text':
        print(value)
    elif fmt == 'html':
        print('<p>%s</p>' % value)

def output_preformatted(fmt, value):
    if fmt == 'text':
        print(value)
    elif fmt == 'html':
        linked = re.sub(r'\((https?\:[\w\d._/?=&]+)\)', r'<a href="\1">\1</a>', value, 0, re.MULTILINE|re.DOTALL)
        print('<pre>%s</pre>' % linked)

def output_seperator(fmt):
    if fmt == 'text':
        print('-------------------------------------------------------------------------------\n')
    elif fmt == 'html':
        print('<hr>')

def output_header(fmt, case):
    h1 = 'Case %s NCC alerts' % case
    if fmt == 'text' and len(case):
        print(h1)
    elif fmt == 'html':
        print('<html>\n<body>\n')
        if len(case):
            output_heading(fmt, 1, h1)

def output_footer(fmt):
    if fmt == 'html':
        print('</body>\n</html>\n')

def key_find_detail(logfile, key, fmt):
    """find the detailed information for a key in the logfile"""
    m = re.search(r'^Detailed information for %s\:(.*?)^(Refer.*?)(^Detailed information for |^\+[-]+)' % key, logfile, re.DOTALL|re.MULTILINE)
    output_heading(fmt, '2', 'NCC check')
    output_paragraph(fmt, 'Detailed information for %s:' % key)

    if m:
        output_preformatted(fmt, m.group(1))
        output_heading(fmt, '2', 'Solution')
        # search for links in the solution section
        output_preformatted(fmt, m.group(2))
    else:
        output_paragraph(fmt, 'Regexp no match for %s' % key)
    output_seperator(fmt)

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
        if re.search(r'^(\/[\w\/]*)\s*$', line):
            prepend = line
            continue
        else:
            prepend = ""
        # check each test to see if it passed
        m = re.search(r'^(\/[\w\/]*)[\s\b]*\[\s*(\w+)\s*\]\s*$', line)
        if m and m.group(2) != "PASS":
            keys.append(os.path.basename(m.group(1)))
                
    return keys

def main():
    #formats = ['text', 'html', 'rtf', 'pdf', 'json', 'md']
    formats = ['text', 'html']
    fmt = 'text'
    case = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:f:h', ['case=', 'format=', 'help'])
    except getopt.GetoptError as err:
        sys.stderr(str(err))
        sys.stderr('for help use --help')
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ('-h', '--help'):
            sys.stderr(__doc__)
            sys.exit(0)
        elif o in ('-f', '--format'):
            if a in formats:
                fmt = a
            else:
                sys.stderr('unknown format: %s' % a)
                sys.ext(3)
        elif o in ('-c', '--case'):
            if len(a):
                case = a
            else:
                sys.stderr('case number required for -c')
                sys.ext(4)
            
    # process arguments
    output_header(fmt, case)

    for arg in args:
        if not os.path.exists(arg):
            sys.stderr("%s not found" % arg)
            continue

        try:
            with open(arg, 'r') as filehandle:
                logfile = filehandle.read()
        except IOError:
            sys.stderr("Could not read %s" % arg)
            sys.exit(5)

        nopass = log_search_no_pass(logfile)
        for key in nopass:
            #look for the output for a particular key
            key_find_detail(logfile, key, fmt)

    output_footer(fmt)

if __name__ == '__main__':
    main()
