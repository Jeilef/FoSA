#!/usr/bin/env python
import subprocess, sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import argparse


def voronoi(input_line, author_changes, lines_history, show):
    with open(input_line, 'r') as target_file:
        target_history = vectorizer.transform([target_file.read()]).toarray()
    np.append(lines_history, target_history)
    dim_reducer = TSNE(random_state=43, n_components=2)
    transformed_authors = dim_reducer.fit_transform(lines_history)
    transformed_document = transformed_authors[-1]
    transformed_authors = transformed_authors[:-1]

    diagram = Voronoi(transformed_authors, incremental=True)
    fig = voronoi_plot_2d(diagram)

    distances = np.linalg.norm([transformed_document - author for author in diagram.points], axis=1)
    nearest_author = np.argmin(distances)
    nearest_author = list(author_changes.keys())[nearest_author]
    print(input_line + ';' + nearest_author)

    if show:
        print(transformed_document)
        plt.plot([transformed_document], "ro")
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser('FSA')
    parser.add_argument('--show', action="store_true", help='show the diagram')
    args = parser.parse_args()

    history = subprocess.run(["git", "log", "-p", "--format=?%an", "--since=1 year ago"], errors='replace', encoding='utf8', capture_output=True, text=True)
    history = history.stdout.split("\n")
    history = [ele for ele in history if ele != ""]
    author_changes = {}
    active_author = ''
    for line in history:
        if line[0] == '?':
            active_author = line[1:]
            author_changes[active_author] = ''
        if line[:2] in ['+ ', '- '] and active_author != '':
            author_changes[active_author] += line.lower()
    vectorizer = CountVectorizer(max_features=256, token_pattern=r'\w+')
    lines_history = vectorizer.fit_transform(author_changes.values()).toarray()

    for il in sys.stdin.readlines():
        input_line = il.strip()
        voronoi(input_line, author_changes, lines_history, args.show)

