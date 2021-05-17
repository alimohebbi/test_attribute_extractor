import re
import glob
from utils import *

def contains_id(line):
    return not re.search(r'R.id\.(.*?)\)', line) is None

def extract_check(value, check):
    if check.startswith("with"):
        value.append({"type":re.search(r'with(.*?)\(', check).group(1).lower(), "value":re.search(r'\"(.*?)\"', check).group(1)})
    else:
        value.append({"type": re.sub('[()]', '', check), "value": ""})
    return value

def extract_checks(line, parsed_event):
    value = []
    match_section = re.search(r'matches\((.*?)\)\);', line.split("check")[1]).group(1)
    if match_section.startswith("allOf"):
        checks = re.search(r'allOf\((.*?)\)\)', match_section).group(1).split(",")
        for check in checks:
            value = extract_check(value, check)         
    else:
        value = extract_check(value, match_section)  
    parsed_event["action"] = [{"type": "check", "value": value}]
    return parsed_event

def extract_perform(line, parsed_event):
    actions = re.search(r'perform\((.*?)\)\;', line).group(1).split(",")
    actions = [action for action in actions if action.replace(" ", "") != "closeSoftKeyboard()"]
    for i in range(len(actions)):
        actions[i] = actions[i].strip(" ")
        if "replaceText" in actions[i]:
            actions[i] = {"type": "replaceText", "value": re.search(r'\"(.*?)\"', actions[i]).group(1)}
        else:
            actions[i] = { "type":actions[i][:-2], "value": ""}
    parsed_event["action"] = actions
    return parsed_event

def extract_action(parsed_event, line):
    #print(line)
    if "onView" not in line:
        if line.replace(" ", "") == "pressBack();":
            parsed_event["action"] = [{"type": "pressBack", "value":""}]
    else:
        if "perform" in line:
            parsed_event = extract_perform(line, parsed_event)            
        elif "check" in line:  
            parsed_event = extract_checks(line, parsed_event)          
    return parsed_event

def extract_get_element_by(parsed_event, line):
    if contains_id(line):
        widget_identifier = "Id"
        value = re.search(r'R.id\.(.*?)\)', line).group(1)
    else:
        widget_identifier = re.search(r'with(.*?)\(', line).group(1)
        value = re.search(r'\"(.*?)\"', line).group(1)
    parsed_event["get_element_by"] = {"type": widget_identifier, "value":value}

    return parsed_event

def rearrange_lines(lines):
    for i, line in enumerate(lines):
        if '=' in line:
            sides = line.split('=')
            variable_name = sides[0].split(' ')[-1]
            if variable_name in lines[i + 1]:
                dot_index = lines[i + 1].find('.')
                lines[i] = lines[i].split("childAtPosition")[0]
                lines[i] += lines[i + 1][dot_index:]
    return lines

def parse_test_section(lines):
    lines = rearrange_lines(lines)
    parsed_event_list = []
    for line in lines:
        if "onView" in line or line.replace(" ", "") == "pressBack();":
            parsed_event = {}
            if "onView" in line:
                new_dict = extract_get_element_by(parsed_event, line)
            parsed_event = extract_action(parsed_event, line)
            parsed_event_list.append(parsed_event)
    return parsed_event_list

def get_test_section(lines):
    seen_test = False
    test = []
    expression = ''
    for line in lines:
        if not seen_test and '@Test' in line:
            seen_test = True
        elif seen_test:
            if "private static Matcher<View> childAtPosition(" in line:
                break
            else:
                expression += line.strip()
                if ';' not in line:
                    continue
                test.append(expression.strip(" ").strip())
                expression = ''
    return test

def parse(fname):
    lines = read_file(fname)
    section = get_test_section(lines)
    parsed_test = parse_test_section(section)
    write_json(parsed_test, fname, '_parsed.json')
    return parsed_test

def main():
    files = glob.glob('../data/*/*/*.java')
    for file in files:
        print(file)
        parse(file)

if __name__ == '__main__':
    main()