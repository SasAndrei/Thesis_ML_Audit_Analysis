import re
import globals as g
import tkinter as tk


AUDIT = ""


def find_variable_value(text, variable):
    pattern = re.compile(r'^\s*(\w+)\s*=\s*' + re.escape(variable) + '[\s.]')
    matches = pattern.findall(text)
    matches = [text for text in matches if text != variable]
    return matches


def get_user_input(input_text):
    root = tk.Tk()
    root.title("Input Window")
    user_input = ""

    label = tk.Label(root, text=input_text)
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text="Submit", command=lambda: [root.quit()])
    button.pack()

    root.minsize(300, 150)  # Set minimum size here (width, height)
    root.mainloop()

    if entry:
        user_input = entry.get()
    root.destroy()
    return user_input


def checklist(file_path):
    file_path.write("##\n")
    file_path.write("# @mainpage Checklist\n")
    empty = 1
    lines = ""
    if g.MODE == "Developer":
        slist = open("../../HelperFiles/DevChecklist.txt", 'w')
        clist = open("../../HelperFiles/Checklist.txt", 'r')
    else:
        clist = open("../../HelperFiles/DevChecklist.txt", 'r')
    for line in clist:
        line = re.sub("\n$", "", line)
        if line == "":
            empty = 1
            file_path.write("# " + line + "\n")
            if g.MODE == "Developer":
                slist.write(line + "\n")
        elif empty == 0:
            file_path.write("# " + line + "\\n\n")
            lines = lines + '\n' + line
            if g.MODE == "Developer":
                slist.write(line + "\n")
        elif re.search(r'^\d+\.', line):
            file_path.write("# " + line + "\\n\n")
            lines = line
            empty = 0
            if g.MODE == "Developer":
                slist.write(line + "\n")
        elif re.search(r'^\|', line):
            if g.MODE in line:
                res = get_user_input(lines + "\n(Y/N/NA)")
                if res == "Y":
                    file_path.write("# | " + g.MODE + " |  | X |  |\n")
                    if g.MODE == "Developer":
                        slist.write("| " + g.MODE + " |  | X |  |\n")
                elif res == "N":
                    file_path.write("# | " + g.MODE + " | X |  |  |\n")
                    if g.MODE == "Developer":
                        slist.write("| " + g.MODE + " | X |  |  |\n")
                else:
                    file_path.write("# | " + g.MODE + " |  |  | X |\n")
                    if g.MODE == "Developer":
                        slist.write("| " + g.MODE + " |  |  | X |\n")
            else:
                file_path.write("# " + line + "\n")
                if g.MODE == "Developer":
                    slist.write(line + "\n")
        else:
            file_path.write("# @section " + re.sub(r"\s", "_", line) + " " + line + "\n")
            if g.MODE == "Developer":
                slist.write(line + "\n")

    file_path.write("##\n\n")


def dataset_analysis(result, notebook):
    global AUDIT
    next_line = 0
    load = ""
    for cell in notebook['cells']:
        content = cell['source']
        if cell['cell_type'] == "code":
            for line in content:
                if "@dataimport" in line:
                    next_line = 1
                elif next_line == 1:
                    load = line
                    break
        if next_line == 1:
            break

    if next_line == 0:
        return
    source = re.search(r"'(.*?)'", load).group(1)
    result.write("\'" + source + "\'")
    if g.MODE == "Developer":
        AUDIT.write("\'" + source + "\'")


def data_type(result):
    global AUDIT
    print(g.PANDAS)
    if g.PANDAS:
        result.write("*Data type text*")
        if g.MODE == "Developer":
            AUDIT.write("*Data type text*")
    else:
        result.write("*Data type image*")
        if g.MODE == "Developer":
            AUDIT.write("*Data type image*")


def auditSheetWrite(file_path, notebook):
    if g.MODE == "Developer":
        template = open("../../HelperFiles/Audit_Sheet_Template.txt", 'r')
        global AUDIT
        AUDIT = open("../../HelperFiles/Dev_Template.txt", 'w')
        file_path.write("\n##\n")
        section = 0
        for line in template:
            line = re.sub("\n$", "", line)
            if re.search("@section", line):
                file_path.write("# " + line + "\n")
                AUDIT.write(line + "\n")
                section = 1
            elif section == 1:
                file_path.write("# " + line + " ")
                AUDIT.write(line + " ")
                audit_line_case(line, file_path, notebook)
                AUDIT.write("\n")
                file_path.write("\\n\n")
            else:
                file_path.write("# " + line + "\n")
                AUDIT.write(line + "\n")
        file_path.write("##\n\n")
    else:
        template = open("../../HelperFiles/Dev_Template.txt", 'r')
        file_path.write("\n##\n")
        section = 0
        for line in template:
            line = re.sub("\n$", "", line)
            if re.search("@section", line):
                file_path.write("# " + line + "\n")
                section = 1
            elif section == 1:
                file_path.write("# " + line + " ")
                file_path.write("\\n\n")
            else:
                file_path.write("# " + line + "\n")
        file_path.write("##\n\n")


def dataSetTracking(result, notebook, val):
    if val == []:
        next_line = 0
        load = ""
        for cell in notebook['cells']:
            content = cell['source']
            if cell['cell_type'] == "code":
                for line in content:
                    if "@dataimport" in line:
                        next_line = 1
                    elif next_line == 1:
                        load = line
                        break
            if next_line == 1:
                break
        source = re.search(r"(^\w+)", load).group(1)
        val.append(source)
        result.write(load)
    else:
        next_line = 0
        load = []
        for cell in notebook['cells']:
            content = cell['source']
            if cell['cell_type'] == "code":
                for line in content:
                    for var in val:
                        temp = find_variable_value(line, var)
                        if temp != []:
                            load = load + temp
                            result.write("## The processed dataset\n")
                            result.write(line)
                            next_line = 1
                    for spl in g.SPLIT:
                        if spl + "(" in line:
                            print(line)
            if next_line == 1:
                break
        val = load

    if val != []:
        g.DATASET = g.DATASET + val
        dataSetTracking(result, notebook, val)


def model_tracking(result, notebook):
    next_line = 0
    current_var = ""
    current_model = ""
    for cell in notebook['cells']:
        content = cell['source']
        if cell['cell_type'] == "code":
            for line in content:
                if "@model" in line:
                    next_line = 1
                elif next_line == 1:
                    current_var = re.findall(r'(\w+)\s*=\s*', line)[0]
                    print(current_var)
                    current_model = re.findall(r'(\w+)\(', line)[0]
                    g.MODELS[current_model] = []
                    g.MODELS[current_model].append(current_var)
                    g.MODELS[current_model].append(re.sub(r"\n$", "", line))
                    next_line = 0
                elif current_var != "" and re.search(r'' + current_var + '(\.|=|\s)', line) and not re.search(r'^#', line) and "import" not in line:
                    g.MODELS[current_model].append(re.sub(r"\n$", "", line))
                else:
                    for ev in g.EVAL:
                        if ev in line and "import" not in line:
                            g.MODELS[current_model].append(re.sub(r"^#", "", re.sub(r"\n$", "", line)))

    keys = g.MODELS.keys()

    result.write("\n##")
    result.write("# @page Models Models\n")

    for k in keys:
        result.write("# @section " + k + " Model is " + k + "\n")
        print(g.MODELS[k])
        for line in g.MODELS[k]:
            result.write("# " + line + "\\n\n")
    result.write("##\n")


def dataset_prelucration(result, notebook):
    for cell in notebook['cells']:
        content = cell['source']
        if cell['cell_type'] == "code":
            for line in content:
                for var in g.DATASET:
                    if var + ".isnull().sum()" in line:
                        for o in range(len(cell["outputs"])):
                            out = cell["outputs"][o]
                            for output in out:
                                # print(output)
                                if output == "data":
                                    outputsdict = out[output]
                                    keys = outputsdict.keys()
                                    for k in keys:
                                        if k == 'text/plain':
                                            res = outputsdict.get(k)
                                            if isinstance(res, list):
                                                result.write("\n\n##\n")
                                                result.write("# @page missing Missing Values\n")
                                                result.write("# Searched for missing values.\n")
                                                result.write("# \n")
                                                result.write("# | Column | Number of missing values | \n")
                                                result.write("# | ------ | ------------------------ | \n")
                                                for r in res:
                                                    for h in g.HEADS:
                                                        if h + " " in r:
                                                            temp = re.sub(h, "", r)
                                                            match = re.search(r'\d+', temp)
                                                            result.write("# | " + h + " | " + match.group() + " | \n")
                                                            g.MISSING = g.MISSING + int(match.group())
                                                result.write("##\n\n")

                    if var + ".info()" in line:
                        for o in range(len(cell["outputs"])):
                            out = cell["outputs"][o]
                            for output in out:
                                if output == "text":
                                    result.write("\n\n##\n")
                                    result.write("# @page description Dataset Description\n")
                                    result.write("# @section info The dataset columns informations\n")
                                    pattern = re.compile(r"(\d+)\s+([^\s]+(?:\s+[^\d\s]+)*)\s+(\d+)\s*(.*)")
                                    result.write("# No. " + re.sub(r"\n$", "", re.sub(r"^\s#", "", out[output][3])) + "\\n\n")
                                    for des in out[output]:
                                        if pattern.search(des):
                                            g.HEADS.append(pattern.search(des).group(2))
                                            result.write("# " + re.sub(r"\n$", "", des) + "\\n\n")
                                    result.write("##\n\n")

                    if var + ".describe" in line:
                        for o in range(len(cell["outputs"])):
                            out = cell["outputs"][o]
                            for output in out:
                                if output == "data":
                                    outputsdict = out[output]
                                    keys = outputsdict.keys()
                                    for k in keys:
                                        res = outputsdict.get(k)
                                        if isinstance(res, list) and k == 'text/plain':
                                            result.write("\n\n##\n")
                                            result.write("# @page description Dataset Description\n")
                                            result.write("# @section description The dataset description\n")
                                            for r in res[:-1]:
                                                temp = re.sub(r"\n$", "", r)
                                                if temp != "":
                                                    if not re.search(r'^[^\s].*', temp):
                                                        header = "| * | "
                                                        blanck = "| - | "
                                                        for d in g.HEADS:
                                                            if d + " " in temp:
                                                                header = header + d + " | "
                                                                blanck = blanck + "- | "
                                                        result.write("# \n")
                                                        result.write("# " + header[:-1] + "\n")
                                                        result.write("# " + blanck[:-1] + "\n")
                                                    else:
                                                        rows = re.findall(r"\b\d+\.\d+\b|\b\w+\b", temp)
                                                        row = "| "
                                                        for h in rows:
                                                            if h != "":
                                                                row = row + h + " | "
                                                        result.write("# " + row[:-1] + "\n")
                                            result.write("##\n\n")


def audit_line_case(line, result, notebook):
    global AUDIT
    if "Data Source" in line:
        dataset_analysis(result, notebook)
    elif "Data Type" in line:
        data_type(result)
    else:
        pass
        # res = get_user_input(line)
        # result.write(res)
        # AUDIT.write(res)
