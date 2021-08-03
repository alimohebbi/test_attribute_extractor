import glob
import os
from utils.utils import *
from utils.configuration import Configuration

config = Configuration()


def extract_selector_list(selector_list, parsed_element):
    keys = parsed_element.keys()
    if "xpath" in keys and parsed_element["xpath"] != "":
        selector_list.append({"type": "xpath", "value": parsed_element["xpath"]})
    if "resource-id" in keys and parsed_element["resource-id"] != "":
        selector_list.append({"type": "resource-id", "value": parsed_element["resource-id"]})
    if "text" in keys and parsed_element["text"] != "":
        selector_list.append({"type": "text", "value": parsed_element["text"]})
    if "content-desc" in keys and parsed_element["content-desc"] != "":
        selector_list.append({"type": "contentDescription", "value": parsed_element["content-desc"]})
    if "class" in keys and parsed_element["class"] != "":
        selector_list.append({"type": "className", "value": parsed_element["class"]})
    return selector_list

def extract_get_element_by(new_parsed_elemetn, parsed_element):
    selector_list = extract_selector_list([], parsed_element)
    new_parsed_elemetn["get_element_by"] = selector_list
    return new_parsed_elemetn


def extract_action_wait(parsed_element, new_parsed_elemetn):
    new_parsed_elemetn["action"] = [parsed_element["action"][0]]
    new_parsed_elemetn["action"].append(parsed_element["action"][1])
    i = 2
    while i < len(parsed_element["action"]):
        if parsed_element["action"][i] == "xpath" and "[@" in parsed_element["action"][i + 1]:
            new_parsed_elemetn["action"].append("class")
            value = parsed_element["action"][i + 1]
            new_parsed_elemetn["action"].append(re.search(r'\/\/(.*?)\[', value).group(1))
            new_parsed_elemetn["action"].append(re.search(r'\@(.*?)\=', value).group(1))
            new_parsed_elemetn["action"].append(re.search(r'\"(.*?)\"', value).group(1))
        else:
            new_parsed_elemetn["action"].append(parsed_element["action"][i])
            new_parsed_elemetn["action"].append(parsed_element["action"][i + 1])
        i += 2
    return new_parsed_elemetn


def extract_action(parsed_element):
    new_parsed_element = {}
    if "action" not in parsed_element.keys():
        return new_parsed_element
    if "wait" in parsed_element["action"][0]:
        new_parsed_element = extract_action_wait(parsed_element, new_parsed_element)
    else:
        new_parsed_element["action"] = []
        for val in parsed_element["action"]:
            new_parsed_element["action"].append(val)
    return new_parsed_element

def get_parsed_file_name(fname):
    return config.parsed_test_dir+"/craftdroid_tests/"+fname.split("/")[-3]+"_"+fname.split("/")[-1].split(".")[0]+'_parsed.json'

def craftdroid_parse(fname):
    parsed_file_name = get_parsed_file_name(fname)
    if os.path.exists(parsed_file_name):
        new_data = load_json_data(parsed_file_name)
    else:
        data = load_json_data(fname)
        new_data = []
        for parsed_element in data:
            new_parsed_elemetn = extract_action(parsed_element)
            if actions_need_element(new_parsed_elemetn["action"]):
                new_parsed_elemetn = extract_get_element_by(new_parsed_elemetn, parsed_element)
            new_data.append(new_parsed_elemetn)
        write_json(new_data, parsed_file_name)
    return new_data


def main():
    craftdroid_globs = config.custom_tests_glob('craftdroid')
    for file in craftdroid_globs:
        craftdroid_parse(file)

if __name__ == '__main__':
    main()
