#!/usr/bin/env python3

import argparse, sys
from matplotlib import pyplot as plt

def is_line_at_ind_zero(line):
    line = line.strip("\n")
    return len(line) == len(line.lstrip())


def is_function_start(line):
    return line.find('def ') == 0


def main(output_file, diagram_type):
    function_meta_data = {}
    for line in sys.stdin:
        with open(line.rstrip("\n\r")) as input_file:
            current_function_name = ''
            functions ={}
            defining_function = False
            function_definition = ''
            for fileline in input_file:
                
                # Stop line counting if line is at ind. zero
                if is_line_at_ind_zero(fileline) and not defining_function: 
                    current_function_name = ''

                # detect if function is starting
                if is_function_start(fileline):
                    function_definition = ''
                    defining_function = True
                    current_function_name = fileline.split('(')[0][4:]
                    functions[current_function_name] = [0, 0]
                
                # collect lines
                if defining_function:
                    function_definition += fileline

                    if (fileline.find(')') != -1):
                        defining_function = False

                        # find number of parameters as soon as full definition is present
                        function_parameters = function_definition.split('(')[1].split(')')[0].strip()
                        number_of_params = 0
                        if function_parameters != '':
                            number_of_params = function_parameters.count(',') + 1
                        functions[current_function_name][1] = number_of_params
                    
                # count lines
                if current_function_name != '' or defining_function:
                    functions[current_function_name][0] += 1
        
            for f in functions.values():
                function_meta_data[f[1]] = function_meta_data.get(f[1], 0) + f[0]
    
    fig = plt.figure(1, figsize=(10, 10))
    if diagram_type == "dot":
        plt.scatter(list(function_meta_data.keys()), list(function_meta_data.values()))
    else:
        plt.boxplot(list(function_meta_data.items()))
    plt.savefig(output_file + '-' + diagram_type + '.pdf', format="pdf")

def test():
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('--output', '-o', type=str, help='filename of output file (pdf)', default='result')
    parser.add_argument('--type', '-t', type=str, choices=['dot', 'box'], help='output format of the diagram', default='dot')
    args = parser.parse_args()
    main(args.output, args.type)