import argparse, csv

ART_SYMBOL = '+'
DELIMITER = '|'
selected_attribute = ''
metrics = []


parser = argparse.ArgumentParser(description='Process some metrics.')
parser.add_argument('file')
parser.add_argument('--attribute', '-a', type=str)
parser.add_argument('--sort', '-s', type=str, choices=['asc', 'desc'])
parser.add_argument('--limit', '-l', type=int)
parser.add_argument('--hierarchical', '-H', action='store_true', default=False)
parser.add_argument('--flat', '-F', action='store_true', default=False)
parser.add_argument('--columns', '-c', type=int, default=80)
args = parser.parse_args()
hierarchical = args.hierarchical and not args.flat

with open(args.file, "r") as file:
    csv_reader = csv.DictReader(file, delimiter=";")
    selected_attribute = csv_reader.fieldnames[1] if args.attribute == None else args.attribute
    for line in csv_reader:
        filename = line[csv_reader.fieldnames[0]]
        if not hierarchical:
            filename = filename.split('/')[-1]
        metrics.append((filename, line[selected_attribute]))

if args.sort is not None:
    metrics = sorted(metrics, key=lambda x: x[1], reverse=(args.sort == 'desc'))

print(args.sort == 'asc')

if args.limit is not None:
    metrics = metrics[:args.limit]
for line in metrics:
    print(line)