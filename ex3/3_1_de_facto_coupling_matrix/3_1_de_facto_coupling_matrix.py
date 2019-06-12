#!/usr/bin/env python3.7

import argparse
import subprocess
import numpy as np
import matplotlib.pyplot as plt

def compute_de_facto_graph(output_file):
    history = subprocess.run(["git", "log", "--format=%ae?%ct", "--name-only"], capture_output=True, text=True)
    history = history.stdout.split("\n")
    history = [ele for ele in history if ele != '']
    de_facto_dict = {}
    current_key = []

    authors = set()
    files = set()

    for line in history:
        if "?" in line:
            split_line = line.split("?")
            split_line[1] = int(split_line[1])/60/60//24 + 0.5
            current_key = tuple(split_line)
            de_facto_dict[current_key] = []
            authors.add(split_line[0])
        else:
            de_facto_dict[current_key].append(line)
            files.add(line)

    de_facto_graph = [[0 for i in range(len(files))] for j in range(len(files))]
    files = list(files)

    for f_mail, f_time in de_facto_dict:
        for s_mail, s_time in de_facto_dict:
            if f_mail == s_mail and f_time != s_time and np.abs(f_time - s_time) <= 3.5*24*60*60:
                f_files = de_facto_dict[f_mail, f_time]
                s_files = de_facto_dict[s_mail, s_time]
                for f_file in f_files:
                    f_index = files.index(f_file)
                    for s_file in s_files:
                        s_index = files.index(s_file)
                        if s_index != f_index:
                            de_facto_graph[f_index][s_index] += 1


    fig, ax = plt.subplots()
    im = ax.imshow(de_facto_graph, cmap='YlGn')
    ax.set_xticks(np.arange(len(files)))
    ax.set_yticks(np.arange(len(files)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(files, fontsize=1)
    ax.set_yticklabels(files, fontsize=1)
    
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False) 
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="left",
             rotation_mode="anchor")

    #fig.tight_layout()
    print("showing file")
    #plt.show()
    plt.savefig(output_file, bbox_inches='tight')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('output', type=str, help='filename of output file (pdf)', default='result.pdf')
    args = parser.parse_args()
    compute_de_facto_graph(args.output)
