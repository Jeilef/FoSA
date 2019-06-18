from collections import Counter
import re, argparse
from os import walk
from sklearn.manifold import MDS
from os.path import join
import matplotlib.pyplot as plt
import random

def compare_files(output_file):
    most_common_words = Counter()
    filenames = []
    for root, dirs, files in walk("."):
        filenames.extend(files)
        for name in files:
            with open(join(root, name), 'r', encoding='utf-8', errors='replace') as file:
                file_words = re.findall(r'\w+', " ".join(file))
                most_common_words.update(file_words)
    bag_of_words = [w for w,c in Counter(most_common_words).most_common(256)]

    file_bags = []
    for root, dirs, files in walk("."):
        for name in files:
            with open(join(root, name), 'r', encoding='utf-8', errors='replace') as file:
                file_bag_of_words_vector = [0] * len(bag_of_words)
                file_words = re.findall(r'\w+', " ".join(file))
                for w in file_words:
                    if w in bag_of_words:
                        index = bag_of_words.index(w)
                        file_bag_of_words_vector[index] += 1
                file_bags.append(file_bag_of_words_vector)
    embedding = MDS(n_components=2, random_state=12)
    reduced_files = embedding.fit_transform(file_bags)
    
    fig, ax = plt.subplots()
    
    xs = []
    ys = []
    for x, y in reduced_files:
        xs.append(x)
        ys.append(y)
    scatter = ax.scatter(xs, ys, s=1)
    for i, txt in enumerate(filenames):
        ax.annotate(txt, (xs[i], ys[i]))
        i += 1
    fig.set_size_inches(20, 10)
    plt.tight_layout()
    plt.savefig(output_file)

if __name__ == "__main__":
    random.seed(12)
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('output', nargs='?', type=str, help='filename of output file (pdf)', default='result.pdf')
    args = parser.parse_args()
    compare_files(args.output)
