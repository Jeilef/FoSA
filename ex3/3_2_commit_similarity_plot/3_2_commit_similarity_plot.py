import subprocess, argparse, re
from collections import Counter

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
    
    print(commits)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('XYZ')
    parser.add_argument('output', type=str, help='filename of output file (pdf)', default='result.pdf')
    args = parser.parse_args()
    compare_commits(args.output)
