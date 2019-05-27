#!/usr/bin/env python3.6

# example usage: ./2_1_per_module_metrics.py

import numpy as np
import os, json, time, re, subprocess

def is_cpp_file(file_name):
    end = file_name.split(".")[-1]
    return end in ["h", "cpp", "hpp", "c"]


file_metrics = {}

for root, dirs, files in os.walk("."):
    for name in files:
        if is_cpp_file(name):
            file_metrics[os.path.join(root, name)] = [365, 0, 0, 0, 0]


# Mean Time Between Changes
history = subprocess.run(["git", "log", "--format=#%ct", "--name-only", "--since=1 year ago "], stdout=subprocess.PIPE)
output = list(filter(lambda x: is_cpp_file(x) and "./" + x in file_metrics, history.stdout.decode('UTF8').split("\n")))
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
        file_metrics["./" + files][0] = int(np.mean(differences) / 60 / 60 / 24)
    else:
        # if file only was changed once we assume MTCB to be the difference between today and the one given date
        file_metrics["./" + files][0] = int((time.time()/1000 - timestamps[0]) / 60 / 60 / 24)

# NUMBER OF AUTHORS
history = subprocess.run(["git", "log", "--format=#%ae", "--name-only", "--since=1 year ago "], stdout=subprocess.PIPE)
output = list(filter(lambda x: is_cpp_file(x) and "./" + x in file_metrics, history.stdout.decode('UTF8').split("\n")))

author_dict = {}
    
for line in output:
    if line[0] == "#":
        current_time = line[1:]
    else:
        author_dict.setdefault(line, set()).add(current_time)

for file, authors in author_dict.items():
    file_metrics['./' + file][1] = len(authors)


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
        file_metrics['./' + os.path.relpath(source_file_name)][3] = object_file_size / source_file_line_count

# Share of Vulkan Code
# only alpha numeric characters and underscore
pattern = re.compile('[\w_]+')
for file in file_metrics.keys():
    with open(file, 'r', encoding='utf-8', errors='replace') as source_file:
        total_symbols = set()
        for line in source_file:
            #print(line, end='')
            symbols = pattern.findall(line.lower())
            total_symbols.update(symbols)
        vk_symbols = 0
        for symbol in total_symbols:
            if len(symbol) > 1 and symbol[:2] == 'vk':
                vk_symbols += 1
        if len(total_symbols) > 0:
            file_metrics[file][4] = vk_symbols / len(total_symbols)
        
# Visualization
print('# filename;MTBC;NoC;BF;OSpLoC;SoVkC')
for filename, metrics in file_metrics.items():
    m = [str(round(i,1)) for i in metrics]
    print(filename + ';' + ";".join(m))
