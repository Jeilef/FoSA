#example usage: git log --format="%an;<%ae>" | python3 1_3_author_consolidation.py

import sys

authors = {}

for line in sys.stdin:
    author = line.split(";")[0]
    mail = line.split(";")[1].split("\n")[0]
    if author in authors:
        if mail not in authors.get(author):
            authors[author].append(mail)
    else:
        authors[author] = [mail]

keys = sorted(authors.keys(), key=lambda k: k.upper())
for k in keys:
    print(k, " ".join(authors.get(k)))