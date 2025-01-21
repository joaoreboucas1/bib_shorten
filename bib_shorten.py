import os
from argparse import ArgumentParser

argp = ArgumentParser()
argp.add_argument("input",                           help="Input .bib file to shorten")
argp.add_argument("-o",               required=True, help="Path to output the shortened bib file", metavar="output")
argp.add_argument("--max-authors",    required=True, help="Maximum number of authors for each entry", type=int, metavar="N")
argp.add_argument("--log",                           help="Whether to log the changes", action="store_true")

def find_cut(string: str, max_authors: int) -> str:
    num_authors = 0
    for i, letter in enumerate(string):
        if letter == "a" and string[i-1].isspace() and string[i:i+3] == "and": 
            num_authors += 1
            if num_authors == max_authors:
                if string[0] == '"': close = '"'
                elif string[0] == '{': close = '}'
                return "      author = " + string[:i+3] + " others" + close + ",\n"

if __name__ == "__main__":
    args = argp.parse_args()
    
    if not os.path.isfile(args.input):
        print(f"ERROR: could not open file {args.input}")
        exit(1)

    with open(args.input, "r") as f:
        lines = f.readlines()

    new_lines = lines
    for i, line in enumerate(lines):
        if "author" in line:
            author, authors = line.strip().split("=")
            num_authors = authors.count("and")
            if num_authors > 5:
                new_authors = find_cut(authors.strip(), max_authors=args.max_authors)
                if args.log:
                    print(f"{args.input}:{i+1}\n{line.strip()} \n>> Shortened to >>\n{new_authors.strip()}")
                    print("--------------")
                new_lines[i] = new_authors


    with open(args.o, "w") as f:
        f.writelines(new_lines)