#!/usr/bin/env python

import subprocess
import numpy as np
import os
import time


def is_cpp_file(file_name):
    end = file_name.split(".")[-1]
    return end in ["h", "cpp", "hpp", "c"]


file_metrics = {}

for root, dirs, files in os.walk("."):
    for name in files:
        if is_cpp_file(name):
            file_metrics[os.path.join(root, name)] = [365, 0, 0, 0, 0]


# Mean Time Between Changes
history = subprocess.run(["git", "log", "--format=#%ct", "--name-only", "--since=\"1 year ago\" "], capture_output=True, text=True)
output = list(filter(lambda x: is_cpp_file(x) and x in file_metrics, history.stdout.split("\n")))
timestamp_dict ={}
current_time = 0

for line in output:
    if line[0] == "#":
        current_time = int(line[1:])
    else:
        timestamp_dict.setdefault(line, []).append(current_time)


for files, timestamps in timestamp_dict.items():
    if len(timestamps) > 1:
        differences = []
        for t_index in range(len(timestamps) - 1):
            diff = timestamps[t_index] - timestamps[t_index + 1]
            differences.append(diff)
        file_metrics[files][0] = int(np.mean(differences) / 60 / 60 / 24)
    else:
        # if file only was changed once we assume MTCB to be the difference between today and the one given date
        file_metrics[files][0] = (int(time.time()) - timestamps[0]) / 60 / 60 / 24

# NUMBER OF AUTHORS
history = subprocess.run(["git", "log", "--format=#%ae", "--name-only", "--since=1 year ago "], capture_output=True, text=True)
output = list(filter(lambda x: is_cpp_file(x) and x in file_metrics, history.stdout.split("\n")))

author_dict = {}

for line in output:
    if line[0] == "#":
        current_time = line[1:]
    else:
        author_dict.setdefault(line, set()).add(current_time)

for file, authors in author_dict.items():
    file_metrics[file].append(len(authors))


# BOTCH FACTOR
for file, metrics in file_metrics.items():
    noc = metrics[1]
    mtbc = metrics[0]
    if mtbc == 0:
        file_metrics[file].append(0)
        continue
    file_metrics[file].append(noc**2//mtbc)

print(file_metrics)

