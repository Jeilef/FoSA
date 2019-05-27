#!/usr/bin/env python3

#example usage: find * -iname "*.py" | ./2_2_function_analysis_tool.py --output result-box.pdf --type box

import argparse, sys
from matplotlib import pyplot as plt

def is_line_at_ind_zero(line):
    line = line.strip("\n")
    return len(line) == len(line.lstrip())

def doSomething ( self, par1, par2, par3, **kwargs):
    """Commentary"""
    result = par1 + par2
    return result

def is_function_start(line):
    return line.find('def ') == 0


def analyse_input():
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

                # count lines
                if current_function_name != '':
                    functions[current_function_name][0] += 1

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
                           
            for f, p in functions.values():
                function_meta_data.setdefault(p, []).append(f)
    return function_meta_data

def visualize_data(data, output_file, diagram_type):
    fig = plt.figure(1, figsize=(10, 10))
    fig.subplots_adjust(top=0.8)
    if diagram_type == "dot":
        x_values = []
        y_values = []
        for key, values in data.items():
            x_values.extend([key] * len(values))
            y_values.extend(values)
        plt.scatter(x_values, y_values)
    else:
        max_parameters = max(data) + 1
        data_list = [[]] * max_parameters
        for key, values in data.items():
            data_list[key] = values
        plt.boxplot(data_list, positions=list(range(max_parameters)), sym='')
    plt.title('Function Analysis')
    plt.xlabel('Number of Parameters')
    plt.ylabel('Lines of Code (per function)')
    plt.savefig(output_file, format="pdf")

if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('--output', '-o', type=str, help='filename of output file (pdf)', default='output.pdf')
    parser.add_argument('--type', '-t', type=str, choices=['dot', 'box'], help='output format of the diagram', default='dot')
    args = parser.parse_args()
    metrics = analyse_input()
    visualize_data(metrics, args.output, args.type)