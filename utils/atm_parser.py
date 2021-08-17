import re
import glob
import os
from utils.utils import *
from utils.configuration import Configuration

config = Configuration()

def remove_child_addressing(line):
    start = line.find("childAtPosition")
    if start == -1:
        return line
    cnt = 1
    for i in range(start + 16, len(line)):
        char = line[i]
        if char == "(":
            cnt += 1
        elif char == ")":
            cnt -= 1
        if cnt == 0:
            end = i
            break
    return line.replace(line[start:end + 2], "")


def get_selector_section(line):
    line = remove_child_addressing(line)
    if "perform" in line:
        selector_section = line.split("perform")[0][:-2]
    elif "check" in line:
        selector_section = line.split("check")[0][:-2]
    elif "pressBack();" in line:
        selector_section = ""
    return selector_section


def contains_id(line):
    return not re.search(r'R.id\.(.*?)\)', line) is None


def add_selector(selector, selector_list):
    if "isDisplayed()" in selector:
        widget_identifier = "isdisplayed"
        value = "true"
    elif contains_id(selector):
        widget_identifier = "resource-id"
        value = re.search(r'R.id\.(.*?)\)', selector).group(1)
    elif "with" in selector:
        widget_identifier = re.search(r'with(.*?)\(', selector).group(1).lower()
        value = re.search(r'\"(.*?)\"', selector).group(1)
    elif "IsInstanceOf" in selector:
        widget_identifier = "classname"
        value = re.search(r'instanceOf\((.*?)\.class', selector).group(1)
    else:
        return selector_list
    selector_list.append({"type": widget_identifier, "value": value})
    return selector_list


def extract_get_element_by(parsed_event, line):
    selector_list = []
    selector_section = get_selector_section(line)
    for selector in selector_section.split(","):
        selector_list = add_selector(selector, selector_list)
    parsed_event["get_element_by"] = selector_list
    return parsed_event


def extract_check(actions, check):
    if re.sub('[ ()]', '', check) == "isDisplayed" or re.sub('[ ()]', '', check) == "isEnabled":
        actions.append(re.sub('[ ()]', '', check))
        actions.append("true")
    else:
        actions.append(re.search(r'with(.*?)\(', check).group(1).lower())
        actions.append(re.search(r'\"(.*?)\"', check).group(1))
    return actions


def extract_checks(line, parsed_event):
    value = []
    match_section = re.search(r'matches\((.*?)\)\);', line.split("check")[1]).group(1)
    actions = ["wait_until_element_presence", 10]
    if match_section.startswith("allOf"):
        checks = re.search(r'allOf\((.*?)\)\)', match_section).group(1).split(",")
        for check in checks:
            actions = extract_check(actions, check)
    else:
        actions = extract_check(actions, match_section)
    parsed_event["action"] = actions
    return parsed_event


def extract_perform(line, parsed_event):
    atm_actions = re.search(r'perform\((.*?)\)\;', line).group(1).split(",")
    atm_actions = [action for action in atm_actions if action.replace(" ", "") != "closeSoftKeyboard()"]
    actions = []
    for i in range(len(atm_actions)):
        atm_actions[i] = atm_actions[i].strip(" ")
        if "replaceText" in atm_actions[i]:
            actions.append("send_keys")
            actions.append(re.search(r'\"(.*?)\"', atm_actions[i]).group(1))
        elif atm_actions[i][:-2] == "longClick":
            actions.append("long_press")
        elif "swipe" in atm_actions[i]:
            direction = atm_actions[i][:-2].split("swipe")[1]
            actions.append("swipe_" + str(direction.lower()))
        else:
            actions.append(atm_actions[i][:-2])
    parsed_event["action"] = actions
    return parsed_event


def extract_action(parsed_event, line):
    if "onView" not in line:
        if "pressBack();" in line:
            parsed_event["action"] = ["KEY_BACK"]
    else:
        if "perform" in line:
            parsed_event = extract_perform(line, parsed_event)
        elif "check" in line:
            parsed_event = extract_checks(line, parsed_event)
    return parsed_event


def rearrange_lines(lines):
    for i, line in enumerate(lines):
        if '=' in line:
            sides = line.split('=')
            variable_name = sides[0].split(' ')[-1]
            if variable_name in lines[i + 1]:
                dot_index = lines[i + 1].find('.')
                lines[i] += lines[i + 1][dot_index:]
    return lines


def parse_test_section(lines):
    lines = rearrange_lines(lines)
    parsed_event_list = []
    for line in lines:
        if "onView" in line or "pressBack();" in line:
            parsed_event = {}
            parsed_event = extract_action(parsed_event, line)
            if actions_need_element(parsed_event["action"]):
                parsed_event = extract_get_element_by(parsed_event, line)
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

def get_parsed_file_name(fname):
    subject_name = fname.split("/")[-1].split(".")[0] + '_parsed.json'
    return os.path.join(config.parsed_test_dir,"/".join(fname.split("/")[-4:-1]),subject_name)

def atm_parse(fname):
    parsed_file_name = get_parsed_file_name(fname)
    lines = read_file(fname)
    section = get_test_section(lines)
    parsed_test = parse_test_section(section)
    # write_json(parsed_test, parsed_file_name)
    return parsed_test

def main():
    atm_globs = config.custom_tests_glob('atm')
    for file in atm_globs:
        atm_parse(file)


if __name__ == '__main__':
    main()