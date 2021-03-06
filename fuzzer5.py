#!/usr/bin/python

# 5-line fuzzer below is from Charlie Miller's
# "Babysitting an Army of Monkeys":
# Part 1 - http://www.youtube.com/watch?v=Xnwodi2CBws
# Part 2 - http://www.youtube.com/watch?v=lK5fgCvS2N

# List of files to use as initial seed
file_list=[
    "doc_files_samples\LiveCode-Reviewers-Guide-April-2013.doc",
    "doc_files_samples\Work Instructions - Rally Naming Conventions.docx",
    "doc_files_samples\Parilak.doc"
    ]

# List of applications to test (vymazal som jednu dalsiu, pouzivam iba jednu a upravil som to dalej v kode)
app = [
     "\Program Files\Microsoft Office\Office14\WINWORD.EXE"
    ]

fuzz_output = "fuzz"

FuzzFactor = 244
num_tests = 10

########### end configuration ##########

import math
import random
import string
import subprocess
import time
import os

crashes = {}

for i in range(num_tests):
    file_choice = random.choice(file_list)
    #app = random.choice(app)

    buf = bytearray(open(file_choice, 'rb').read())

    # start Charlie Miller code
    numwrites=random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)
    #end Charlie Miller code

    with open(fuzz_output, "wb") as f:
        f.write(buf)
 
    print "Opening file '%s' with app '%s', %d bytes changed" % (file_choice, app, numwrites)
 
    p = subprocess.Popen([app, fuzz_output])
    time.sleep(3)
 
    crashed = p.poll()
    if not crashed:
        p.terminate()
    else:
        crashes[app] += 1
 
 
print "Test summary"
print "=" * 40
for app, count in crashes.items():
    print "App '%s' crashed %d times." % (app, count)