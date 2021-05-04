import re

def contains_id(line):
        return not re.search(r'R.id\.(.*?)\)', line) is None

def extract_get_element_by(new_dict, line):
        if contains_id(line):
            identifier = "Id"
            value = re.search(r'R.id\.(.*?)\)', line).group(1)
        else:
            identifier = re.search(r'with(.*?)\(', line).group(1)
            value = re.search(r'\"(.*?)\"', line).group(1)
        new_dict["get_element_by"] = [identifier, value]

        return new_dict

def extract_action(new_dict, line):
        if "onView" not in line:
            line = line.replace(" ", "")
            if line == "pressBack();":
                new_dict["action"] = ["pressBack()"]
        else:
            if "perform" in line:
                actions = re.search(r'perform\((.*?)\)\;', line).group(1).split(",")
                for i in range(len(actions)):
                    actions[i] = actions[i].strip(" ")
                    if "replaceText" in actions[i]:
                        actions[i] = {"replaceText()": re.search(r'\"(.*?)\"', actions[i]).group(1)}
                new_dict["action"] = actions
            elif "check" in line:
                new_dict["action"] = ["check()"]
        return new_dict

def get_test_section(lines):
        seen_test = False
        test = []
        expression = ''
        for line in lines:
            if not seen_test and '@Test' in line:
                seen_test = True
            elif seen_test:
                if '{' in line:
                    continue
                elif '}' in line:
                    break
                else:
                    expression += line.strip()
                    if ';' not in line:
                        continue
                    test.append(expression.strip(" ").strip())
                    expression = ''
        return test

def parse_test_section(lines):
        dicts = []
        for i, line in enumerate(lines):
            if '=' in line:
                sides = line.split('=')
                variable_name = sides[0].split(' ')[-1]
                if variable_name in lines[i + 1]:
                    dot_index = lines[i + 1].find('.')
                    lines[i].replace(';', '')
                    lines[i] += lines[i + 1][dot_index:]
        for line in lines:
            if "onView" in line or line.replace(" ", "") == "pressBack();":
                new_dict = {}
                if "onView" in line:
                    new_dict = extract_get_element_by(new_dict, line)

                new_dict = extract_action(new_dict, line)
                dicts.append(new_dict)
        return dicts

def parse(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    section = get_test_section(lines)
    return parse_test_section(section)