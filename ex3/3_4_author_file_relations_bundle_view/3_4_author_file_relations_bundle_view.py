import subprocess, argparse


def author_file_relations(outputfile):
    history = subprocess.run(["git", "log", "--format=?%ct?%ae", "--name-only"], capture_output=True, text=True)
    history = list(filter(lambda x: x != "", history.stdout.split("\n")))

    base_data = []

    for line in history:
        if line[0] == "?":
            splitted_line = line.split("?")
            timestamp = splitted_line[1]
            author = splitted_line[2]
        else:
            base_data.append([int(timestamp), author, line])

    noc_author = {}
    noc_file = {}
    mtbc_author = {}
    mtbc_file = {}

    for time, author, file in base_data:
        noc_author[author] = noc_author.setdefault(author, 0) + 1
        noc_file[file] = noc_file.setdefault(file, 0) + 1

        mtbc_author.setdefault(author, []).append(time)
        mtbc_file.setdefault(file, []).append(time)

    mtbc_author = mtbc_on_dict(mtbc_author)
    mtbc_files = mtbc_on_dict(mtbc_file)

    with open(outputfile, "w+") as vis_file:
        vis_file.write("hierarchy;authors;" + str(len(mtbc_author)) + "\n")
        for author in mtbc_author:
            vis_file.write("node;author;" + str(author) + ";" + str(noc_author[author]) + ";" + str(mtbc_author[author]) + "\n")
        vis_file.write("hierarchy;modules;" + str(len(mtbc_file)))
        for module in mtbc_files:
            vis_file.write("node;module;" + str(module) + ";" + str(mtbc_files[module]) + ";" + str(mtbc_files[module]) + "\n")
        vis_file.write("edges;edits;" + str(len(base_data)) + "\n")

        for _, author, module in base_data:
            vis_file.write("edge;edit;" + author + ";" + module + "\n")


def mtbc_on_dict(dictionary):
    mtbc_dict = {}
    for author, timestamps in dictionary.items():
        # assuming mtbc 0 when only one change
        if len(timestamps) == 1:
            mtbc_dict[author] = 0
            continue
        timestamps.sort()
        diff = 0
        for i, t in enumerate(timestamps[:-1]):
            diff += timestamps[i+1] - timestamps[i]
        mtbc_dict[author] = diff/(len(timestamps) - 1)
    return mtbc_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('output', type=str, help='filename of output file (pdf)',nargs="?" , default='graph.txt')
    args = parser.parse_args()
    author_file_relations(args.output)