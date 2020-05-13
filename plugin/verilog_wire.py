#!/usr/bin/env python3

"""this script is a basic script for doing verilog editing
it parses the variables from stdin and generate a verilog name instantiation
of the variables"""

import re
import sys

skip_last_coma = 0
if len(sys.argv) > 1:
    skip_last_coma = int(sys.argv[1])

keywords = []
keywords.extend(["input", "output", "inout", "ref", "parameter", "localparam"])
keywords.extend(["reg", "logic", "wire", "bit", "integer", "int", "string", "type"])
keywords.extend(["const", "unsigned"])

patterns = []
patterns.append(re.compile(r'\[[^\[\]]*\]'))  # port size, array size
patterns.append(re.compile(r'=.*'))           # assignment
patterns.append(re.compile(r'//.*'))          # // comment
patterns.append(re.compile(r'\w+\.\w+'))      # interfaces with modport
for kw in keywords:                           # match keywords
    patterns.append(re.compile("\\b%s\\b" % kw))

pattern_empty_line = re.compile(r'^\s*$')
pattern_open_comment = re.compile(r'/\*.*')
pattern_close_comment = re.compile(r'.*\*/')
pattern_open_to_close_comment = re.compile(r'/\*.*\*/')
pattern_punctuation = re.compile(r'[,;]')
pattern_two_words_no_coma = re.compile(r'^\s*(\w+)\s+(\w+.*)')
pattern_spaces = re.compile(r'\s+')

ports = []
wait_to_close_comment = 0
indent_len = -1

for line in sys.stdin:
    # print(line)
    # get indentation length from 1st non empty line
    if indent_len == -1 and not(pattern_empty_line.match(line)):
        indent_len = len(re.match(r'^\s*', line).group(0))
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

    # delete input or output
    line = line.replace("input",  " ")
    line = line.replace("output", "")
    if "wire" not in line:
        if "reg" in line:
            line = line.replace("reg", "wire")
        else:
            line = "wire "+line
    
    line = line.replace(",", ";")
    line = line.strip()
    if line=="":
        continue
    if line[-1] != ";":
        line = line + ";"

    print(line)
