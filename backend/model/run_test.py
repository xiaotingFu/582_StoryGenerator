#!/usr/bin/env python
import subprocess
import sys
import os
# import time
print("Start running the story generator")

p = subprocess.Popen("python model/run.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p.wait()
with open('../db/output.txt') as f:
    story = f.read()
    print(story)
# time.sleep(90)
# for line in p.stdout.readlines():
#     print(line)
sys.stdout.flush()
