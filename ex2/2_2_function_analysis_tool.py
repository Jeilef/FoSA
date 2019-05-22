import argparse, sys

def main(output_file, diagram_type):
    for line in sys.stdin:
        with open(line.rstrip("\n\r")) as input_file:
            linecount = 0
            for fileline in input_file:
                if len(fileline) == len(fileline.lstrip()) or fileline.lstrip() == '':
                    print(linecount)    
                    if fileline.find('def ') != -1:
                        print (fileline.rstrip(), end=' ')
                    linecount = 0
                else:
                    linecount += 1
            print(linecount)

def test():
    pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('--output', '-o', type=str, help='filename of output file (pdf)', default='2-2-function-analysis.pdf')
    parser.add_argument('--type', '-t', type=str, choices=['dot', 'box'], help='output format of the diagram', default='dot')
    args = parser.parse_args()
    main(args.output, args.type)