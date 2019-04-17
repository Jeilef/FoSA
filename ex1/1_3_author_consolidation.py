import sys

authors = {}

for line in sys.stdin:
    author = line.split(";")[0]
    mail = line.split(";")[1].split("\n")[0]
    if author in authors:
        print(author)
        print(mail)
        print(authors.get(author))
        if mail not in authors.get(author):
            authors[author] = authors[author].append(mail)
    else:
        authors[author] = [].append(mail)
        if author == "Allan Sandfeld Jensen":
            print(authors.get("Allan Sandfeld Jensen"))


print(authors.get("Allan Sandfeld Jensen"))

for k in authors:
    print(k, " ".join(authors.get(k)))