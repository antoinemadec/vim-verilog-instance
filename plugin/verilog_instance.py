#!/usr/bin/env python3

# this script is a basic script for doing verilog editing
# it parses the variables from stdin and generate a verilog name instantiation
# of the variables

import re
import sys

keywords = []
keywords.extend([ "input", "output", "inout", "ref", "parameter", "localparam" ])
keywords.extend([ "reg", "wire", "bit", "integer", "int", "string", "unsigned" ])

patterns = []
patterns.append(re.compile('\[.*\]'))   # port size, array size
patterns.append(re.compile('=.*'))      # assignment
patterns.append(re.compile('[,;]'))     # end of line punctuation
for kw in keywords:                     # match keywords
    patterns.append(re.compile("\\b%s\\b" % kw))
patterns.append(re.compile('\s+'))      # spaces and end of line

ports = []
for line in sys.stdin:
    for pattern in patterns:
        line = pattern.sub(' ', line)
    ports.extend(line.strip().split(' '))

max_str_len = len(max(ports, key=len))

for port in ports:
    space_str = " " * (max_str_len - len(port))
    print(".%s%s (%s%s)," % (port,space_str,port,space_str))
