from os import walk

for dirpath, dnames, fnames in walk("."):
    for filename in fnames:
        line_count = 0
        for line in open(dirpath + "/" +  filename, encoding='utf8', errors='replace'):
            line_count+=1
        print(filename + ';' + str(line_count))