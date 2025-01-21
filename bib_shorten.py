file_name = "nls.bib"
with open(file_name, "r") as f:
    lines = f.readlines()

def find_cut(string: str) -> str:
    num_authors = 0
    max_authors = 5
    for i, letter in enumerate(string):
        if letter == "a" and string[i-1].isspace() and string[i:i+3] == "and": 
            num_authors += 1
            if num_authors == max_authors:
                if string[0] == '"': close = '"'
                elif string[0] == '{': close = '}'
                return "      author = " + string[:i+3] + " others" + close + ",\n"

count = 0
new_lines = lines
for i, line in enumerate(lines):
    if "author" in line:
        author, authors = line.strip().split("=")
        num_authors = authors.count("and")
        if num_authors > 5:
            new_authors = find_cut(authors.strip())
            print(f"{i} : {authors} \n=>\n{new_authors}")
            new_lines[i] = new_authors
            print("--------------")
        count += 1

output_file_name = "nls_short.bib"
with open(output_file_name, "w") as f:
    f.writelines(new_lines)