import subprocess, argparse, re
from collections import Counter
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import random

random.seed(43)

# This requires matplotlib version 3.1.0
def compare_commits(output_file):
    history = subprocess.run(["git", "log", "-p", "--format=?%ae"], capture_output=True, text=True)
    history = history.stdout.split("\n")
    history = [ele for ele in history if ele != ""]
    author_history = [ele[1:] for ele in history if ele[0] == '?']
    words_history = [ele.lower() for ele in history if ele[:2] == '+ ']
    words = re.findall(r'\w+', " ".join(words_history))
    most_common_words = [w for w,c in Counter(words).most_common(256)]

    current_commit = ''
    commits = []
    for line in history:
        if line[0] != "?" and line[:2] == '+ ':
            current_commit += line
        elif line[0] == "?":
            line_words = re.findall(r'\w+', current_commit)
            bag_of_words_vector = [0] * len(most_common_words)
            for w in line_words:
                if w in most_common_words:
                    index = most_common_words.index(w)
                    bag_of_words_vector[index] += 1
            commits.append(bag_of_words_vector)
            current_commit = ""

    pca = PCA(n_components=2, random_state=43)
    reduced_commits = pca.fit_transform(commits)

    unique_authors = np.unique(author_history)
    c = np.random.rand(len(unique_authors))

    fig, ax = plt.subplots()
    author_colors = []
    for u_author in author_history:
        a_index = list(unique_authors).index(u_author)
        author_colors.append(c[a_index])

    xs = []
    ys = []
    for x, y in reduced_commits:
        xs.append(x)
        ys.append(y)
    scatter = ax.scatter(xs, ys, c=author_colors, s=1)
    handles, labels = scatter.legend_elements(num=len(unique_authors))
    plt.legend(handles, unique_authors, loc='center left', bbox_to_anchor=(1, 0.2))
    fig.set_size_inches(20, 10)
    plt.tight_layout()
    plt.savefig(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('output', type=str, help='filename of output file (pdf)',nargs="?" , default='result.pdf')
    args = parser.parse_args()
    compare_commits(args.output)
