import subprocess

print("Start running the story generator")
p = subprocess.Popen('python run.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)
retval = p.wait()
