#!/usr/bin/env python3

# this script is a basic script for doing verilog editing
# it parses the variables from stdin and generate a verilog name instantiation
# of the variables

import re
import sys

keywords = []
keywords.extend([ "input", "output", "inout", "ref", "parameter", "localparam" ])
keywords.extend([ "reg", "wire", "bit", "integer", "int", "string", "type" ])
keywords.extend([ "unsigned" ])

patterns = []
patterns.append(re.compile('\[.*\]'))   # port size, array size
patterns.append(re.compile('=.*'))      # assignment
patterns.append(re.compile('[,;]'))     # end of line punctuation
patterns.append(re.compile('//.*'))     # // comment
for kw in keywords:                     # match keywords
    patterns.append(re.compile("\\b%s\\b" % kw))
patterns.append(re.compile('\s+'))      # spaces and end of line

pattern_open_comment          = re.compile('/\*.*')
pattern_close_comment         = re.compile('.*\*/')
pattern_open_to_close_comment = re.compile('/\*.*\*/')

pattern_empty_line = re.compile('^\s*$')

ports                 = []
wait_to_close_comment = 0
indent_len            = -1

for line in sys.stdin:
    # get indentation length from 1st non empty line
    if indent_len == -1 and not(pattern_empty_line.match(line)):
            indent_len = len(re.match('^\s*', line).group(0))
    # handle comments
    if wait_to_close_comment:
        if pattern_close_comment.search(line):
            line = pattern_close_comment.sub(' ', line)
            wait_to_close_comment = 0
        else:
            continue
    if pattern_open_comment.search(line):
        if pattern_close_comment.search(line):
            line = pattern_open_to_close_comment.sub(' ', line)
        else:
            wait_to_close_comment = 1
            continue
    # handle all other patterns
    for pattern in patterns:
        line = pattern.sub(' ', line)
    # add port names
    line = line.strip()
    if line != "":
        ports.extend(line.split(' '))

if len(ports) > 0:
    max_str_len = len(max(ports, key=len))
    for port in ports:
        space_str = " " * (max_str_len - len(port))
        indent_str = " " * indent_len
        print("%s.%s%s (%s%s)," % (indent_str,port,space_str,port,space_str))
