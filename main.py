import os
from pathlib import Path
import re
import json
import ast
from audit_analysis import *
import globals as g
import racer as ontology


def get_library_links(content):
    pattern = re.compile(r'(\w+)\.\w+')
    matches = []
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []
    links = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "pandas":
                    g.PANDAS = True
                matches = pattern.findall(alias.name)
                if matches:
                    links.append(f"https://pypi.org/project/{matches[0]}/")
                else:
                    links.append(f"https://pypi.org/project/{alias.name}/")
        elif isinstance(node, ast.ImportFrom):
            # Use the module name instead of node.names to construct the link
            if node.module == "pandas":
                g.PANDAS = True
            matches = pattern.findall(node.module)
            if matches:
                links.append(f"https://pypi.org/project/{matches[0]}/")
            else:
                links.append(f"https://pypi.org/project/{node.module}/")

    return list(set(links))


def replace_links(text):
    pattern = r'\[([^]]+)\]\([^)]+\)'  # pattern to match "[Link Name](Link URL)"
    match = re.search(pattern, text)
    while match:
        link_name = match.group(1)
        text = text.replace(match.group(0), link_name)
        match = re.search(pattern, text)
    return text


def clean_text(rgx_list, text):
    new_text = text
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text


def markdown_level(my_string):
    count = 0
    while my_string.startswith("#", count):
        count += 1
    if count == 0:
        return 100
    return count - 1


def remove_spaces_and_hashes(s):
    while s and (s[0] == " " or s[0] == "#" or s[0] == '\n'):
        s = s[1:]
    return s


def check_string(string):
    stack = []
    quotes = None

    for char in string:
        if char in ('(', '[', '{'):
            stack.append(char)
        elif char in (')', ']', '}'):
            if not stack:
                return False
            if char == ')' and stack[-1] != '(':
                return False
            if char == ']' and stack[-1] != '[':
                return False
            if char == '}' and stack[-1] != '{':
                return False
            stack.pop()
        elif char in ('"', "'"):
            if not quotes:
                quotes = char
            elif quotes == char:
                quotes = None

    return not stack and not quotes


def parsPyFile(files):
    result = open("result_py.py", 'w')
    result.write("##\n")
    result.write("# @file result_py.py \n")
    result.write("##\n")
    line = files.readline()
    section = 0
    while line:
        if re.search("^#", line):
            if re.search("^##", line):
                section = (section + 1) % 2
                if section == 0:
                    result.write(line + "\n")
                else:
                    result.write(line)
            else:
                result.write(line)
        line = files.readline()
    result.write("\n")
    result.close()


def parsIpynbFile(files):
    result = open("result_ipynb.py", 'w')
    result.write("##\n")
    result.write("# @file result_ipynb.py \n")
    result.write("##\n\n")
    notebook = json.load(files)
    # mainp = 0
    count = 0
    i = 0
    current_level = 100
    code_line = ""

    while i < len(notebook["cells"]):
        cell = notebook["cells"][i]
        if cell["cell_type"] == "markdown":
            content = cell["source"]
            level = markdown_level(content[0])
            title = remove_spaces_and_hashes(content[0])
            title = re.sub(r"\n$", "", title)
            title = clean_text([r"\*", r"`"], title)
            if title != "":
                if current_level != 100 and level <= current_level:
                    result.write("##\n\n")
                if level != 100:
                    title = replace_links(title)
                    if level <= current_level:
                        result.write("##\n")
                        result.write("# @page commentNo." + str(count) + " " + title + "\n")
                        current_level = level
                    else:
                        result.write("#\n")
                        result.write("# @section sectionNo" + str(count) + " " + title + "\n")
                        result.write("#\n")
                else:
                    result.write("#\n")

            for line in content:
                line = remove_spaces_and_hashes(line)
                line = re.sub(r"\n$", "", line)
                if line != "":
                    result.write("# " + line + "\n")
            j = i + 1
            links = []
            while j < len(notebook["cells"]):
                next_cell = notebook["cells"][j]
                if next_cell["cell_type"] == "markdown":
                    break
                elif next_cell["cell_type"] == "code":
                    codecell = code_line.join(next_cell["source"])
                    links = links + get_library_links(codecell)
                    if next_cell["outputs"]:
                        for o in range(len(next_cell["outputs"])):
                            out = next_cell["outputs"][o]
                            for output in out:
                                if output == "data":
                                    outputsdict = out[output]
                                    keys = outputsdict.keys()
                                    for k in keys:
                                        if "image/" in k:
                                            img = re.sub(r"\n$", "", outputsdict.get(k))
                                            result.write("# @image html \"data:image/png;base64," + img + "\"\n")
                                            # result.write("# @image latex \"data:image/png;base64," + outputsdict.get(k) + "\"\n")
                j += 1
            i = j
            if links:
                result.write("# \\n\n")
                result.write("# @section imports Libraries imported in this section: \n")
                for link in links:
                    match = re.search(r'/(\w+)/$', link)
                    if match:
                        library = match.group(1)
                        result.write("# Librry " + library + ": ")
                    result.write(" " + link + "\\n\n")
            count = count + 1
        else:
            i += 1
    result.write("##\n\n")

    for cell in notebook['cells']:
        content = cell['source']
        if cell['cell_type'] == "code":
            save_next = 0
            save_line = ""
            for line in content:
                if re.search("^#", line):
                    # result.write("\n#" + line)
                    save_line = line
                    save_next = 1
                elif save_next == 1 and re.search(r"^\s*\w+\s*=\s*[\w\"']+", line):
                    result.write("\n#" + save_line)
                    save_line = ""
                    if check_string(line):
                        save_next = 0
                        result.write(line)
                    else:
                        code_line = remove_spaces_and_hashes(re.sub(r"\n$", "", line))
                        save_next = 2
                elif save_next == 2:
                    code_line = code_line + remove_spaces_and_hashes(re.sub(r"\n$", "", line))
                    if check_string(code_line):
                        save_next = 0
                        result.write(code_line)
                        code_line = ""
    result.write("\n")
    auditSheetWrite(result, notebook)
    dataset_analysis(result, notebook)
    dataSetTracking(result, notebook, [])
    dataset_prelucration(result, notebook)
    model_tracking(result, notebook)
    checklist(result)
    result.close()

    with open('result_ipynb.py', 'r') as input_file:
        lines = input_file.readlines()

    filtered_lines = []
    skip = 0

    for i in range(0, len(lines) - 3):
        if lines[i].endswith('##\n') and lines[i + 3].endswith('##\n'):
            skip += 3
        elif skip != 0:
            skip -= 1
        else:
            filtered_lines.extend(lines[i])

    with open('result_ipynb.py', 'w') as output_file:
        output_file.writelines(filtered_lines)
    # print("Searched = " + str(ontology.searchItem("SQL")))
    print(g.MISSING)
    g.reset_globals()


def doxygenFile(filename):
    result = open("Doxyfile", 'w')
    result.write("PROJECT_NAME = \"" + filename + "\"\n")
    result.write("PROJECT_NUMBER = \"1.0\"\n")
    result.write("OUTPUT_DIRECTORY = \"docs\"\n")
    result.write("INPUT = result_" + extension + ".py\n")
    result.write("GENERATE_LATEX = YES\n")
    result.write("LATEX_OUTPUT = latex\n")
    result.write("LATEX_CMD_NAME = pdflatex\n")
    # result.write("LATEX_EXTRA_FILES = mystyle.sty\n")
    result.write("EXTRACT_ALL = NO\n")
    result.write("FILTER_SOURCE_FILES = YES\n")
    result.write("OPTIMIZE_OUTPUT_JAVA = YES\n")
    result.write("HIDE_UNDOC_MEMBERS = YES\n")
    result.close()
    os.system("doxygen")


if __name__ == '__main__':
    mode = get_user_input("Choose mode run programm:\nDeveloper(D)\nAudit(A)")
    if "D" in mode:
        g.mode("Developer")
    else:
        g.mode("Audit")
    Path("results").mkdir(parents=True, exist_ok=True)
    for filename in os.listdir("target"):
        file = open("target/" + filename, 'r')
        name, extension = filename.split(".")
        Path("./results/docs_" + extension + "_" + name).mkdir(parents=True, exist_ok=True)
        os.chdir("./results/docs_" + extension + "_" + name)
        if re.search(".py$", filename):
            parsPyFile(file)
            # doxygenFile(filename)
        else:
            parsIpynbFile(file)
            doxygenFile(filename)
        os.chdir("../..")
