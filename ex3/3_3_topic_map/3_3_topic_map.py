from collections import Counter
from os import walk

def compare_files(output_file):
    for root, dirs, files in os.walk(".", topdown=False):
        with
        words_history = [ele.lower() for ele in history if ele[:2] == '+ ']
    words = re.findall(r'\w+', " ".join(words_history))
    most_common_words = [w for w,c in Counter(words).most_common(256)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('output', type=str, help='filename of output file (pdf)', default='result.pdf')
    args = parser.parse_args()
    compare_files(args.output)
