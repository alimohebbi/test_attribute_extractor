import json
import pathlib

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
    f = open(fname, )
    data = json.load(f)
    return data


def get_capabilities(app_package, app_activity, no_reset):
    caps = {
        'platformName': 'Android',
        'platformVersion': '6.0',
        'deviceName': '2.7_QVGA_API_23',
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
        if category == "craftdroid_tests" or category == "test_repo":
            return fname.split("/")[-1].split(".")[0]
        else:
            return None


def get_package_activity(fname):
    app_name = get_app_name(fname)
    if app_name is None:
        return None, None
    activity_file_path = str(pathlib.Path(__file__).parent.absolute()) + "/../app_name_to_package_activity.csv"
    df = pd.read_csv(activity_file_path)
    sliced_df = df[df["appName"] == app_name]
    if len(sliced_df) == 0:
        print("No application with the name : " + str(app_name) + " can be found in app_name_to_package_activity.csv.")
        return None, None
    app_package = sliced_df.iloc[0]["appPackage"]
    app_activity = sliced_df.iloc[0]["appActivity"]
    no_reset = sliced_df.iloc[0]["noReset"]

    return app_package, app_activity, no_reset


def get_caps(fname):
    app_package, app_activity, no_reset = get_package_activity(fname)
    if no_reset == 0:
        caps = get_capabilities(app_package, app_activity, False)
    else:
        caps = get_capabilities(app_package, app_activity, True)
    return caps, app_package


def preprocess_text(s):
    return " ".join(re.sub(r'[^\w\s]', '', s.lower()).split())


def actions_need_element(action):
    if action[0] not in ["KEY_BACK", "wait_until_text_invisible"]:
        return True
    return False
