import pandas as pd
import glob
import json
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import time

def write_to_error_log(message, filename):
    f = open(filename, 'a')
    f.write(message)

def write_json(data, fname, name_postfix):
    with open(fname.replace('.json', name_postfix), 'w') as f:
        f.write(json.dumps(data, indent=2))
def load_json_data(fname):
    f = open(fname,)
    data = json.load(f)
    return data

def get_app_name(fname):
    app_name = fname.split("/")[-1].split(".")[0]
    return app_name

def get_package_activity(fname, df):
    app_name = get_app_name(fname)
    app_package = list(df[df["appName"] == app_name]["appPackage"])[0]
    app_activity = list(df[df["appName"] == app_name]["appActivity"])[0]

    return app_package, app_activity

def reparse_element_actions(parsed_element, log_fname):
    new_dict = {}
    action = parsed_element["action"][0]
    print(action)
    if action == "click" or action == "long_press" or action.startswith("swipe"):
        new_dict["type"] = action
        new_dict["value"] = ""
    elif "send_keys" in action:
        new_dict["type"] = action
        new_dict["value"] = parsed_element["action"][1]
    elif action.startswith("wait"):
        new_dict["type"] = action
        new_dict["value"] = {"time":parsed_element["action"][1],\
        "type": parsed_element["action"][2], "value": parsed_element["action"][3]}
    elif action == "KEY_BACK":
        new_dict["type"] = "pressback"
        new_dict["value"] = ""
    else:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnhandled action: "+str(action[0])+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        new_dict = None
    return [new_dict]
    
def reparse_element(parsed_element, log_fname):
    new_parsed_elemetn = {}
    if("resource-id" in parsed_element.keys() and parsed_element["resource-id"]!=""):
        new_parsed_elemetn["get_element_by"] = {"type": "Id", "value":parsed_element["resource-id"]}
    elif("xpath" in parsed_element.keys() and parsed_element["xpath-id"]!=""):
        new_parsed_elemetn["get_element_by"] = {"type": "XPath", "value":parsed_element["xpath"]}
    elif("text" in parsed_element.keys() and parsed_element["text"]!=""):
        new_parsed_elemetn["get_element_by"] = {"type": "Text", "value":parsed_element["text"]}
    elif("content-desc" in parsed_element.keys() and parsed_element["content-desc"]!=""):
        new_parsed_elemetn["get_element_by"] = {"type": "ContentDescription", "value":parsed_element["content-desc"]}
    elif("class" in parsed_element.keys() and parsed_element["class"]!=""):
        new_parsed_elemetn["get_element_by"] = {"type": "ClassName", "value":parsed_element["class"]}
    else:
        ("NONE OF THE ABOVE")
    new_parsed_elemetn["action"] = reparse_element_actions(parsed_element, log_fname)
    return new_parsed_elemetn
    
def reparse_data(fname, log_fname):
    data = load_json_data(fname)
    new_data = []
    for parsed_element in data:
        new_parsed_elemetn = reparse_element(parsed_element, log_fname)
        print("new_parsed_elemetn")
        print(new_parsed_elemetn)
        print()
        new_data.append(new_parsed_elemetn)
    write_json(new_data, fname, '_reparsed.json')
    return new_data

def read_file(file):
    log_fname = file.replace('.json', "_log.txt")
    data = reparse_data(file, log_fname)
    print("data")
    df = pd.read_csv("app_name_to_package_activity.csv")
    app_package, app_activity = get_package_activity(fname, df)
    caps = {
        'platformName': 'Android',
        'platformVersion': '7.0',
        'deviceName': 'emulator-5555',
        'appPackage': app_package,
        'appActivity': app_activity,
        'autoGrantPermissions': True,
        'noReset': False,
        "newCommandTimeout": 3000
    }
    return data, caps, log_fname

def execute_action(driver, el, dictionary, log_fname):
    executed = True
    for action in dictionary["action"]:
        
        if "send_keys" in action["type"]:
            el.send_keys(action["value"])
            if "enter" in action["type"]:
                driver.press_keycode(66)
            if "hide_keyboard" in action["type"]:
                if driver.is_keyboard_shown():
                    driver.back()
     
        elif action["type"].startswith("swipe"):
            direction = action["type"].split("_")[1]
            print("direction")
            
            if direction == "right":
                end_x = driver.get_window_size()["width"]
                end_y = el.location['y']
                
            elif direction == "left":
                end_x = 0
                end_y = el.location['y']
                
            if direction == "up":
                end_x = el.location['x']
                end_y = 0
                
            if direction == "down":
                end_x = el.location['x']
                end_y = driver.get_window_size()["height"]
                
            TouchAction(driver).press(el).move_to(el, end_x, end_y).release().perform()
        
        elif action["type"] == "click":
            el.click()
            
        elif action["type"] == "long_press":
            TouchAction(driver).long_press(el).perform()
            
        elif action["type"] == "pressback":
            driver.back()
            
        elif action["type"] == "wait_until_element_presence":
            continue
            
        elif action["type"] == "wait_until_text_presence":
            #WebDriverWait(driver, action["value"]["time"]).until(EC.presence_of_element_located((By.TEXT,\
            #    action["value"]["value"])))
            time.sleep(10)
            try:
                waiting_element = get_element_by_text(driver, action["value"]["value"], log_fname)
            except:
                waiting_element = None
            if waiting_element is None:
                error_message = 40*"#"+" ERROR! "+40*"#"+"\nThe element with the text: " + action["value"]["value"] + ", did not appear after"+str(action["value"]["time"])+"seconds."
                write_to_error_log(error_message, log_fname)
                print(error_message)
            #continue
            
        elif action["type"] == "wait_until_text_invisible":
            #WebDriverWait(driver, action["value"]["time"]).until(EC.presence_of_element_located((By.TEXT,\
            #    action["value"]["value"])))
            time.sleep(10)
            try:
                waiting_element = get_element_by_text(driver, action["value"]["value"], log_fname)
            except:
                waiting_element = None
            if waiting_element is not None:
                error_message = 40*"#"+" ERROR! "+40*"#"+"\nThe element with the text: " + action["value"]["value"] + ", did not get invisible after"+str(action["value"]["time"])+"seconds."
                write_to_error_log(error_message, log_fname)
                print(error_message)
            #continue
        else:
            executed = False
            error_message = 40*"#"+" ERROR! "+40*"#\nUnknown event: "+str(action["type"])
            write_to_error_log(error_message, log_fname)
    return executed

def get_element_actions(dictionary):
    actions = []
    for action in dictionary["action"]:
        if action["type"] == "send_keys_and_enter":
            actions.append(action["type"]+":"+action["value"])
        else:
            actions.append(action["type"])
    return actions

def get_element_attributes(element, dictionary):

    element_attributes = {}
    
    attribute_list =  ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
    "focused","long-clickable", "package", "password", "resource-id", "scrollable","selection-start",
    "selection-end", "selected", "text", "bounds", "displayed"]
    
    for attr in attribute_list:
        element_attributes[attr] = element.get_attribute(attr)
    
    actions = get_element_actions(dictionary)
    element_attributes["action"] = actions
    return element_attributes

def get_element_by_id(driver, resource_id, log_fname):
    try:
        element =  driver.find_element_by_id(resource_id)
        return element
    except NoSuchElementException:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with id: " + resource_id + ", found on this page source."
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_content_desc(driver, content_desc, log_fname):
    try:
        element = driver.find_element_by_android_uiautomator('new UiSelector().description(\"'+content_desc+'\")')
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with content description: " + content_desc + ", found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_text(driver, text, log_fname):
    try:
        element = driver.find_element_by_android_uiautomator('new UiSelector().text(\"'+text+'\")')
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with text: " + text + ", found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_xpath(driver, xpath, log_fname):
    try:
        element = driver.find_element_by_xpath(xpath)
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with xpath: " + xpath + ", found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_class_name(driver, class_name, log_fname):
    try:
        element = driver.find_element_by_class_name(class_name)
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with class name: " + class_name + ", found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None
def get_element(driver, dictionary, log_fname):
    identifier = dictionary["get_element_by"]["type"]
    value = dictionary["get_element_by"]["value"]
    if identifier == "Id":
        element = get_element_by_id(driver, value, log_fname)    
    elif identifier == 'ContentDescription':
        element = get_element_by_content_desc(driver, value, log_fname)   
    elif identifier == "Text":
        element = get_element_by_text(driver, value, log_fname)   
    elif identifier == "XPath":
        element = get_element_by_xpath(driver, value, log_fname)   
    elif identifier == "ClassName":
        element = get_element_by_class_name(driver, value, log_fname)   
    else:
        print(40*"# ERROR! "+40*"#")
        print("Unknown identifier of the element in line: " + str(dictionary))
        return None
    return element

def get_attribute_list(parsed_test, driver, log_fname):
    attribute_list = []
    completed = True
    for line in parsed_test:
        print(line)
        print()
        el = get_element(driver, line, log_fname)
        if el is None:
            completed = False
            attribute_list.append({})
            continue
        attributes = get_element_attributes(el, line)
        attribute_list.append(attributes)
        executed = execute_action(driver, el, line, log_fname)
        if not executed:
            completed = False
            break
        time.sleep(5)
    return attribute_list, completed

def main():
    files = glob.glob('data/test_repo/*/b*2/base/*.json')
    for file in files:
        start_time = time.time()
        print(file.split("/")[-1])
        data, caps, log_fname = read_file(file)
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
        except:
            continue
        attribute_list, completed = get_attribute_list(data, driver, log_fname)
    	write_json(attribute_list, fname, "_attributes.json")
        print(str(time.time() - start_time)+" seconds\n")

if __name__ == '__main__':
    main()