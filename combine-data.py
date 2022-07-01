"""
Usage: $ python combine-data.py data > data-combined.yml
"""

import glob
import sys
import os

folder = sys.argv[-1]
assert os.path.isdir(folder), f"folder {folder} does not exist"

pattern = os.path.join(folder, "*.yml")

print("---")
for yaml_file in sorted(glob.glob(pattern)):
    with open(yaml_file, "r") as f:
        for i, line in enumerate(f.read().splitlines()):
            if i == 1:
                record = line.split()[-1]
                print(f"{record}:")
            if i > 1:
                print(f"  {line}")
