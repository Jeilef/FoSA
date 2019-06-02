#!/usr/bin/env python3.6

# example usage: ./2_1_per_module_metrics.py

import numpy as np
import os, json, time, re, subprocess

def is_cpp_file(file_name):
    end = file_name.split(".")[-1]
    return end in ["h", "cpp", "hpp", "c"]


def transform_file_paths(output, lookup):
    transformed_files = []
    for o in output:
        if "#" not in o:
            new_file = os.path.relpath(o)
            if new_file in lookup:
                transformed_files.append(new_file)
        else:
            transformed_files.append(o)
    return transformed_files


file_metrics = {}
file_path_start = ""
for root, dirs, files in os.walk("."):
    file_path_start = root[:2]
    for name in files:
        if is_cpp_file(name):
            # we set default values for the 5 metrics
            # MTBC : 365 => Biggest possible interval in our timeframe, since our observed time is one year
            # NoC : 0 => No commits = No authors
            # BF : 0 => 0 / 365 = 0
            # OSpLoC : 0 => No object file => 0 Bytes / LoC = 0
            # SoVkC : 0 => No symbols found that start with vk
            file_metrics[os.path.relpath(os.path.join(root,name))] = [365, 0, 0, 0, 0]

# Mean Time Between Changes
# We assume a MTBC for Files with only one change during our timeframe from the date of the commit to the current date
# We also assume a MTBC for Files with no commits of our max interval of 1 year 
history = subprocess.run(["git", "log", "--format=#%ct", "--name-only", "--since=1 year ago "], stdout=subprocess.PIPE)
history = history.stdout.decode('UTF8').split("\n")
output = list(filter(lambda x: is_cpp_file(x) or '#' in x, history))
output = transform_file_paths(output, file_metrics)

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
        file_metrics[files][0] = int((time.time() - timestamps[0]) / 60 / 60 / 24)

# NUMBER OF AUTHORS
history = subprocess.run(["git", "log", "--format=#%ae", "--name-only", "--since=1 year ago "], stdout=subprocess.PIPE)
history = history.stdout.decode('UTF8').split("\n")
output = list(filter(lambda x: is_cpp_file(x) or '#' in x, history))
output = transform_file_paths(output, file_metrics)


author_dict = {}
current_author = ''
    
for line in output:
    if line[0] == "#":
        current_author = line[1:]
    else:
        author_dict.setdefault(line, set()).add(current_author)

for file, authors in author_dict.items():
    file_metrics[file][1] = len(authors)


# BOTCH FACTOR
for file, metrics in file_metrics.items():
    noc = metrics[1]
    mtbc = metrics[0]
    if mtbc != 0:
        file_metrics[file][2] = noc**2 / mtbc

#Object Size per LoC 
with open('./compile_commands.json') as json_file:
    file_mapping = json.load(json_file)
    for compile_entry in file_mapping:
        working_directory = compile_entry['directory']
        source_file_name = compile_entry['file']
        source_file_line_count = 0
        with open(source_file_name) as source_file:
            source_file_line_count = len(list(enumerate(source_file))) 
        object_file_name = compile_entry['command'].split('-o ')[1].split(' ')[0]
        object_file_size = os.path.getsize(os.path.join(working_directory, object_file_name))
        file_metrics[os.path.relpath(source_file_name)][3] = object_file_size / source_file_line_count

# Share of Vulkan Code
# only alpha numeric characters and underscore
pattern = re.compile('[\w_]+')
for file in file_metrics.keys():
    with open(file, 'r', encoding='utf-8', errors='replace') as source_file:
        # We assume that 'This check is case-insensitive and 
        # counts every occurrence of a symbol per source code file' 
        # means total number of symbols, not the total number of unique symbols
        total_symbols = []
        for line in source_file:
            symbols = pattern.findall(line.lower())
            total_symbols.extend(symbols)
        vk_symbols = 0
        for symbol in total_symbols:
            if len(symbol) > 1 and symbol[:2] == 'vk':
                vk_symbols += 1
        if len(total_symbols) > 0:
            file_metrics[file][4] = vk_symbols / len(total_symbols)
        
# Visualization
print('# filename;MTBC;NoC;BF;OSpLoC;SoVkC')
for filename, metrics in file_metrics.items():
    m = [str(round(i,2)) for i in metrics]
    print(filename + ';' + ";".join(m))
