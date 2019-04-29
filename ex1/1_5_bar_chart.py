import argparse, csv, sys

ART_SYMBOL = '+'
DELIMITER = ' | '
selected_attribute = ''
metrics = []

# Example Usage: python3 1_5_bar_chart.py --sort=desc --limit=10 --columns=100 < merged-metrics.csv

parser = argparse.ArgumentParser(description='Process some metrics.')
parser.add_argument('--attribute', '-a', type=str)
parser.add_argument('--sort', '-s', type=str, choices=['asc', 'desc'])
parser.add_argument('--limit', '-l', type=int)
parser.add_argument('--hierarchical', '-H', action='store_true', default=False)
parser.add_argument('--flat', '-F', action='store_true', default=False)
parser.add_argument('--columns', '-c', type=int, default=80)
args = parser.parse_args()
hierarchical = args.hierarchical and not args.flat

with sys.stdin as file:
    csv_reader = csv.DictReader(file, delimiter=";")
    selected_attribute = csv_reader.fieldnames[1] if args.attribute is None else args.attribute
    for line in csv_reader:
        filename = line[csv_reader.fieldnames[0]]
        attribute_value = line[selected_attribute]
        if not hierarchical:
            filename = filename.split('/')[-1]
        if attribute_value is not '':
            metrics.append((filename, float(attribute_value)))

if args.sort is not None:
    metrics = sorted(metrics, key=lambda x: x[1], reverse=(args.sort == 'desc'))

if args.limit is not None:
    metrics = metrics[:args.limit]

max_len = 0
max_value = 0
for line in metrics:
    max_len = max(max_len, len(line[0]))
    max_value = max(max_value, line[1])

remaining_symbols = args.columns - max_len

for line in metrics:
	padding = ' ' * (max_len - len(line[0]))
	ascii_art = ""
	if(max_value == 0):
		ascii_art = ART_SYMBOL * int(remaining_symbols)		
	else:
		ascii_art = ART_SYMBOL * int(line[1] / max_value * remaining_symbols)
	print(padding + line[0] + DELIMITER + ascii_art)