#!/usr/bin/env python
from optparse import OptionParser
from sys import stdout, stdin, stderr
from codecs import open as copen
from sdag2 import DAG, CycleDetectedException
from re import split

usage = "usage: %prog [options] [FILE [OUT_FILE]]"
parser = OptionParser(usage=usage)
parser.add_option("-f", "--file", dest="filename",
                  help="With no FILE, or when FILE is -, read standard input.",
                  metavar="FILE", default="STDIN")
parser.add_option("-o", "--out-file", dest="out_filename",
                  help="Write result to OUT_FILE, default is standard output.",
                  metavar="OUT_FILE", default="STDOUT")
parser.add_option("-s", "--separator", dest="separator",
                  help="Items separator, default is \s regex.",
                  metavar="SEP", default="\s")
parser.add_option("-q", "--quit-sequence", dest="quit_sequence",
                  help="Stop read FILE where line equals QUIT_SEQ, default "
                  "is %default.",
                  metavar="QUIT_SEQ", default=":quit")

(options, args) = parser.parse_args()

if len(args) > 0:
    options.filename = args[0]
    
    if len(args) > 1:
        options.out_filename = args[1]

if options.filename in ("STDIN", "-", ""):
    inf = stdin
else:
    inf = copen(options.filename, "rb")

if options.out_filename in ("STDOUT", "-", ""):
    outf = stdout
else:
    outf = copen(options.out_filename, "wb")

dag = DAG()

line = inf.readline()
i = 0

while line:
    line = line.strip()
    i += 1
    if not line:
        stderr.write("[WARN]: Line %s is empty.\n" % i)
        continue
    elif line == options.quit_sequence:
        break
    
    parts = split(options.separator, line)

    try:    
        if len(parts) == 2:
            dag.add_edge(parts[0], parts[1])
        elif len(parts) == 1:
            dag.add(parts[0])
        else:
            stderr.write("[ERROR]: Line %s contains more 2 items.\n" % i)
            exit(1)
        
        line = inf.readline()
    except CycleDetectedException as ex:
        stderr.write("[ERROR]: %s.\n" % ex)
        exit(1)

for l in dag.topologicaly(gen=True):
    outf.write(l)
    outf.write("\n")
