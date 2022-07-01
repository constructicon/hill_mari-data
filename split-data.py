"""
Usage: $ python split-data.py data-combined.yml data

This will write the data files to the folder `data`, you can change the
name/location.
"""

import sys
import os
from collections import defaultdict

data_file = sys.argv[-2]
assert os.path.exists(data_file), f"file {data_file} does not exist"

folder = sys.argv[-1]
if not os.path.exists(folder):
    os.makedirs(folder)

data = defaultdict(list)

with open(data_file, "r") as f:
    for line in f.read().splitlines():
        if line.startswith("---"):
            pass
        elif not line.startswith("  "):
            record_number = int(line.split(":")[0])
        else:
            data[record_number].append(line)

for (k, vs) in data.items():
    output_file = os.path.join(folder, f"{k:04d}.yml")
    vs_without_two_spaces = map(lambda s: s[2:], vs)
    with open(output_file, "w") as f:
        f.write("---\n")
        f.write(f"record: {k}\n")
        f.write("\n".join(vs_without_two_spaces))
        f.write("\n")
