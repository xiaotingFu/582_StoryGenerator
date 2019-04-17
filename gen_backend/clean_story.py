import hashlib

out_file = 'output.txt'
in_file = 'input.txt'

completed_lines_hash = set()

o_file = open(out_file, 'w')

for line in open(in_file, 'r'):
    hash_value = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()

    if hash_value not in completed_lines_hash:
        o_file.write(line)
        completed_lines_hash.add(hash_value)

o_file.close()
