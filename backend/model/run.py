#!/usr/bin/env python
import json
import sys
import gen_backend.final_story
import subprocess
subprocess.call("../gen_backend/final_story.py", shell=True)
with open('../db/output.txt') as f:
    story = f.read()
    print(story)
sys.stdout.flush()

