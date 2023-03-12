#!/usr/bin/env python3

"""this script is a basic script for doing verilog editing
it parses the variables from stdin and generate a verilog name instantiation
of the variables"""

import re
import sys

skip_last_coma = 0
keep_comment = 1
keep_empty_line = 1
if len(sys.argv) > 1:
    skip_last_coma = int(sys.argv[1])

if len(sys.argv) > 2:
    keep_comment = int(sys.argv[2])

keywords = []
keywords.extend(["input", "output", "inout", "ref", "parameter", "localparam"])
keywords.extend(["reg", "logic", "wire", "bit", "integer", "int", "string", "type"])
keywords.extend(["const", "unsigned"])

patterns = []
patterns.append(re.compile(r'\[[^\[\]]*\]'))  # port size, array size
patterns.append(re.compile(r'=.*'))           # assignment
patterns.append(re.compile(r'//.*') )
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

pattern_inline_comment_kept = re.compile(r'.*\w+.*(//.*)')      # comment in port define
pattern_comment_kept = re.compile(r'\s*(//.*)')               # one line comment

ports = []
ports_comments = {}   # save comment for every port
contents = []          # save ports and single line comments
wait_to_close_comment = 0
indent_len = -1

for line in sys.stdin:
    # get indentation length from 1st non empty line
    if indent_len == -1 and not(pattern_empty_line.match(line)):
        indent_len = len(re.match(r'^\s*', line).group(0))
    # handle empty line
    if pattern_empty_line.match(line) is not None:
        contents.append('')
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
    # handle port comment
    port_comment = pattern_inline_comment_kept.match(line)
    if port_comment is not None:
        port_comment = port_comment.group(1)
    # handle single line comment
    line_comment = pattern_comment_kept.match(line)
    if line_comment is not None:
        line_comment = line_comment.group(1)
    # handle all other patterns
    for pattern in patterns:
        line = pattern.sub(' ', line)
    # handle typedef, class and interfaces
    line = pattern_two_words_no_coma.sub('\\2', line)
    line = pattern_punctuation.sub(' ', line)
    line = pattern_spaces.sub(' ', line)
    # finally, get port names
    line = line.strip()
    if line != "":
        port_names = line.split(' ')
        ports.extend(port_names)
        contents.extend(port_names)
        for port in port_names:
                ports_comments[port] = port_comment
    else:
        # add single line comment to port
        if line_comment is not None:
                contents.append(line_comment)

ports_nb = len(ports)
i = 0
if ports_nb > 0:
    max_str_len = len(max(ports, key=len))
    indent_str = " " * indent_len
    for content in contents:
        if len(content) > 0:
            if content[:2] == "//":
                if keep_comment == 1:
                    print(f'{indent_str}{content}')
                continue
        else:
            # empty line
            if keep_empty_line == 1:
                print('')
            continue
        port = content
        skip_coma = skip_last_coma and i == (ports_nb - 1)
        space_str = " " * (max_str_len - len(port))
        output_line_port = "%s.%s%s (%s%s)%s" % (
            indent_str, port, space_str, port, space_str, (",", "")[skip_coma])
        if ports_comments.get(port) is not None and keep_comment == 1:
            # add port comment
            output_line = f"{output_line_port}  {ports_comments.get(port)}"
        else:
            output_line = output_line_port
        print(output_line)
        i = i + 1
