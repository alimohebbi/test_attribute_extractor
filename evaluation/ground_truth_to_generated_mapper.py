from typing import List, Dict, Tuple
import toml
import json
import glob
import pandas as pd

with open('../config_template/config.toml', 'r') as file:
    config = toml.load(file)
ALGORITHM = str(config["algorithm"])


def atm_subject(filename):
    filename = filename.split('/')[-2].split("-")[0]
    return filename.startswith("a6") or filename.startswith("a7") or filename.startswith("a8")


def change_nulls_to_empty_strings(json_list: List[Dict[str, object]]) -> List[Dict[str, object]]:
    if json_list is None:
        return json_list
    new_json_list = []
    for obj in json_list:
        for k, v in obj.items():
            if v is None:
                obj[k] = ""
        new_json_list.append(obj)
    return new_json_list


def empty_event(parsed_element):
    keys = parsed_element.keys()
    if "class" in keys and parsed_element["class"] == "EMPTY_EVENT":
        return True
    return False

def remove_extra_events(generated: List[Dict[str, object]]) -> List[Dict[str, object]]:
    if generated is None:
        return generated
    generated = [x for x in generated if not empty_event(x)]
    generated = [x for x in generated if not x["action"][0].startswith("wait") and not x["action"][0] == "KEY_BACK"]
    return generated


def get_gt_filename(filename: str) -> str:
    if ALGORITHM == "craftdroid":
        if atm_subject(filename):
            gt_filename = filename.split('/')[-2] + ".json"
        else:
            gt_filename = '-'.join(filename.split('/')[-2].split("-")[-2:]) + ".json"
    else:
        gt_filename = filename.split('/')[-2] + "_attributes.json"
    return gt_filename
    

def find_ground_truth(filename: str) -> str:
    gt_filename = get_gt_filename(filename)
    files = glob.glob(config[ALGORITHM]['GROUND_TRUTH_GLOBE']['address'])
    for file in files:
        if gt_filename in file:
            return file
    return None
    

def load_json_file(file_address: str) -> list:
    json_file: List[Dict[str, object]] = None
    with open(file_address, 'r') as f:
        json_file = json.load(f)
    json_file = remove_extra_events(json_file)
    json_file = change_nulls_to_empty_strings(json_file)
    return json_file


def load_json_files(file: str, gt_file_address: str) -> Tuple[list, list]:
    generated = load_json_file(file)
    ground_truth = load_json_file(gt_file_address)

    return generated, ground_truth


def drop_craftdroid_attributes(obj: dict) -> dict:
    craftdroid_extra_attributes = ["tid", "parent_text", "sibling_text", "ignorable",\
    "stepping_events", "state_score", "score", "selected", "checkable", "checked", "selection-start",\
    "enabled", "long-clickable", "scrollable", "package", "activity", "event_type",\
    "naf", "clickable", "displayed", "focusable", "focused", "password", "selection-end"]
    for attribute in craftdroid_extra_attributes:
        try:
            obj.pop(attribute)
        except KeyError:
            pass
    return obj


def drop_extra_attributes(obj: dict, file: str) -> dict:
    try:
        if "_and_hide_keyboard" in obj["action"][0]:
            obj["action"][0] = obj["action"][0].split("_and_hide_keyboard")[0]
    except KeyError:
        pass
    try:
        obj.pop('page')
    except KeyError:
        pass
    try:
        obj.pop('bounds')
    except KeyError:
        pass
    if ALGORITHM == "craftdroid":
        obj = drop_craftdroid_attributes(obj)
    return obj


def ordered(obj) -> str:
    if obj is None:
        return obj
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return [ordered(x) for x in obj]
    else:
        return str(obj).lower().strip()


def get_src_and_tgt(file: str) -> Tuple[str, str]:
    migration = file.split('/')[-2] 
    src_app = migration.split('-')[0]
    tgt_app = migration.split('-')[1]
    if ALGORITHM == "craftdroid":
        src_app = src_app + "-" + migration.split('-')[2]
        tgt_app = tgt_app + "-" + migration.split('-')[2]
    return src_app, tgt_app


def add_corresponding_objects_to_map(result: pd.core.frame.DataFrame,
                                     file: str,
                                     generated: list,
                                     ground_truth: list) -> pd.core.frame.DataFrame:
    src_app, tgt_app = get_src_and_tgt(file)
    for i, gt in enumerate(ground_truth):
        gt = drop_extra_attributes(gt, file)
        equal_gens = []
        for j, gen in enumerate(generated):
            gen = drop_extra_attributes(gen, file)
            if ordered(gen) == ordered(gt):
                equal_gens.append(str(j))
        result.loc[len(result)] = [src_app, tgt_app, i, ' '.join(equal_gens)]
    return result


def extract_ground_truth_generated_map(files: list, migration_config: str):
    result = pd.DataFrame(columns=['src_app', 'target_app', 'src_index', 'target_index'])
    for file in files:
        gt_file_address = find_ground_truth(file)
        if gt_file_address is None:
            continue
        generated, ground_truth = load_json_files(file, gt_file_address)
        if generated is None or ground_truth is None:
            continue
        result = add_corresponding_objects_to_map(result, file, generated, ground_truth)

    result.to_csv(config[ALGORITHM]['gt_gen']['address'] + migration_config + ".csv", index=False)


def extract_all_ground_truth_generated_maps():
    migration_configs = glob.glob(config[ALGORITHM]['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        migration_config = migration_config.split("/")[-1]
        files = glob.glob(
            config[ALGORITHM]['BASE_JSON_ADDRESS']['generated'] + migration_config + "/*/*.json")
        extract_ground_truth_generated_map(files, migration_config)


def main():
    extract_all_ground_truth_generated_maps()


if __name__ == '__main__':
    main()
