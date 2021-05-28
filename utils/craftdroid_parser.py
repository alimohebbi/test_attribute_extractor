import glob
from utils.utils import *

def extract_selector_list(selector_list, parsed_element, log_fname):
	keys = parsed_element.keys()
	if("xpath" in keys and parsed_element["xpath"]!=""):
		selector_list.append({"type": "xpath", "value":parsed_element["xpath"]})
	if("resource-id" in keys and parsed_element["resource-id"]!=""):
		selector_list.append({"type": "resource-id", "value":parsed_element["resource-id"]})
	if("text" in keys and parsed_element["text"]!=""):
		selector_list.append({"type": "text", "value":parsed_element["text"]})
	if("content-desc" in keys and parsed_element["content-desc"]!=""):
		selector_list.append({"type": "contentdescription", "value":parsed_element["content-desc"]})
	if("class" in keys and parsed_element["class"]!=""):
		selector_list.append({"type": "classname", "value":parsed_element["class"]})	
	return selector_list

def extract_get_element_by(new_parsed_elemetn, parsed_element, log_fname):  
	selector_list = extract_selector_list([], parsed_element, log_fname) 
	if len(selector_list) == 0 and actions_need_element(new_parsed_elemetn["action"]):
		error_message = 40*"#"+" ERROR! "+40*"#"+"\nFor the element : "+str(parsed_element)+", there are no selectors by which we can find the element.\n\n\n"
		write_to_error_log(error_message, log_fname)
	new_parsed_elemetn["get_element_by"] = selector_list
	return new_parsed_elemetn

def extract_wait_actions(new_parsed_elemetn, parsed_element, log_fname):
    action = parsed_element["action"][0]
    new_parsed_elemetn["action"].append({"type": "wait", "value": parsed_element["action"][1]-5})
    if action == "wait_until_text_presence":
        new_parsed_elemetn["action"].append({"type": "check","value": [{"type": parsed_element["action"][2], "value": parsed_element["action"][3]}]})
    elif action == "wait_until_text_invisible":
        new_parsed_elemetn["action"].append({"type": "check_element_invisible","value": [{"type": parsed_element["action"][2], "value": parsed_element["action"][3]}]})
    elif action == "wait_until_element_presence":
        new_parsed_elemetn["action"].append({"type": "check_element_presence","value": [{"type": parsed_element["action"][2], "value": parsed_element["action"][3]}]})
    else:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnhandled wait action: "+str(action)+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return new_parsed_elemetn

def extract_send_keys_actions(new_parsed_elemetn, parsed_element, log_fname):
	action = parsed_element["action"][0]
	if "clear" in action:
		new_parsed_elemetn["action"].append({"type": "clear", "value": ""})
	new_parsed_elemetn["action"].append({"type": "replaceText", "value": parsed_element["action"][1]})
	if "enter" in action:
		new_parsed_elemetn["action"].append({"type": "enter", "value": ""})
	return new_parsed_elemetn

def extract_action(parsed_element, log_fname):
	new_parsed_elemetn = {}
	if "action" not in parsed_element.keys():
		return new_parsed_elemetn
	action = parsed_element["action"][0]
	new_parsed_elemetn["action"] = []
	if action == "click":
		new_parsed_elemetn["action"].append({"type": "click", "value": ""})
	elif action == "long_press":
		new_parsed_elemetn["action"].append({"type": "longClick", "value": ""})
	elif action == "KEY_BACK":
		new_parsed_elemetn["action"].append({"type": "pressBack", "value": ""})
	elif action.startswith("swipe"):
		new_parsed_elemetn["action"].append({"type": action.replace("_", ""), "value": ""})
	elif "send_keys" in action:
		new_parsed_elemetn = extract_send_keys_actions(new_parsed_elemetn, parsed_element, log_fname) 
	elif "wait" in action:
		new_parsed_elemetn = extract_wait_actions(new_parsed_elemetn, parsed_element, log_fname)       
	else:
		error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnhandled action: "+str(action)+"\n\n\n"
		write_to_error_log(error_message, log_fname)
	return new_parsed_elemetn

def craftdroid_parse(fname):
	log_fname = fname.replace(fname.split("/")[-1], "atm_compatible/"+fname.split("/")[-1].split(".")[0]+"_parse_log.txt")
	data = load_json_data(fname)
	new_data = []
	for parsed_element in data:
		new_parsed_elemetn = extract_action(parsed_element, log_fname)
		new_parsed_elemetn = extract_get_element_by(new_parsed_elemetn, parsed_element, log_fname)
		new_data.append(new_parsed_elemetn)
	write_json(new_data, fname.replace(fname.split("/")[-1], "atm_compatible/"+fname.split("/")[-1].split(".")[0]+"_reparsed.json"))
	return new_data

def main():
    files = glob.glob('../data/craftdroid_tests/*/*/*/*.json')
    for file in files:
        print(file)
        craftdroid_parse(file)

if __name__ == '__main__':
    main()