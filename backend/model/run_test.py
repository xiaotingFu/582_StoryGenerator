#!/usr/bin/env python
import subprocess
import sys

print("Start running the story generator")
p = subprocess.Popen('python mode/run.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()
sys.stdout.flush()
