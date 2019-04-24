#!/usr/bin/env python
import subprocess
import sys
import os
print("Start running the story generator")

p = subprocess.Popen(["python", "model/run.py"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()
sys.stdout.flush()
