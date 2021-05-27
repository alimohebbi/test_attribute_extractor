import json
import pandas as pd
import re

def read_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    return lines

def write_to_error_log(message, filename):
    f = open(filename, 'a')
    f.write(message)
    print(message)
    
def write_json(data, new_name):
    with open(new_name, 'w') as f:
        f.write(json.dumps(data, indent=2))
        
def load_json_data(fname):
    f = open(fname,)
    data = json.load(f)
    return data

def get_capabilities(app_package, app_activity, no_reset):
    caps = {
        'platformName': 'Android',
        'platformVersion': '7.0',
        'deviceName': 'emulator-5555',
        'appPackage': app_package,
        'appActivity': app_activity,
        'autoGrantPermissions': True,
        'noReset': no_reset,
        "newCommandTimeout": 3000
    }
    return caps

def get_app_name(fname):
    category = fname.split("/")[-3]
    if category == "migrated_tests":
        return fname.split("/")[-2].split("-")[1]
    elif category == "donor":
        return fname.split("/")[-2]
    else:
        category = fname.split("/")[-5]
        if category == "craftdroid_tests":
            return fname.split("/")[-1].split(".")[0]
        else:
            print("Application not recognized!"+"\n"+"The test file should be under directory \"/data/migrated_tests\",  \"/data/ground_truth\" or \"/data/craftdroid_tests\"")
            return None

def get_package_activity(fname):
    app_name = get_app_name(fname)
    if app_name is None:
        return None, None
    df = pd.read_csv("app_name_to_package_activity.csv")
    sliced_df = df[df["appName"] == app_name]
    if len(sliced_df) == 0:
        print("No application with the name : "+str(app_name)+" can be found in app_name_to_package_activity.csv.")
        return None, None
    app_package = sliced_df.iloc[0]["appPackage"]
    app_activity = sliced_df.iloc[0]["appActivity"]

    return app_package, app_activity

def get_caps(fname): 
    app_package, app_activity = get_package_activity(fname)
    caps = get_capabilities(app_package, app_activity, False)
    return caps, app_package

def preprocess_text(s):
    return re.sub(r'[^\w\s]', '', s.lower()).split()