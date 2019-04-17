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

for k in authors:
    print(k, " ".join(authors.get(k)))