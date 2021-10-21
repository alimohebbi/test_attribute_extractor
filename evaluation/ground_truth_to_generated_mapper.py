from typing import List, Dict, Tuple
import toml
import json
import glob
import pandas as pd

with open('config.toml', 'r') as file:
    config = toml.load(file)
ALGORITHM = str(config["algorithm"])


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


def remove_oracles(generated: List[Dict[str, object]]) -> List[Dict[str, object]]:
    if generated is None:
        return generated
    generated = [x for x in generated if not x["action"][0].startswith("wait")]
    return generated


def get_gt_filename(filename: str) -> str:
    if ALGORITHM == "craftdroid":
        gt_filename = '-'.join(filename.split('/')[-2].split("-")[-2:]) + "_attributes.json"
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
    

def load_json_files(file: str, gt_file_address: str) -> Tuple[list, list]:
    generated: List[Dict[str, object]] = None
    with open(file, 'r') as f:
        generated = json.load(f)
    generated = remove_oracles(generated)
    generated = change_nulls_to_empty_strings(generated)

    ground_truth: List[Dict[str, object]] = None
    with open(gt_file_address, 'r') as f:
        ground_truth = json.load(f)
    ground_truth = change_nulls_to_empty_strings(ground_truth)

    return generated, ground_truth


def drop_page_bounds(obj: dict) -> dict:
    try:
        obj.pop('page')
    except KeyError:
        pass
    try:
        obj.pop('bounds')
    except KeyError:
        pass
    return obj


def ordered(obj) -> str:
    if obj is None:
        return obj
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return [ordered(x) for x in obj]
    else:
        return str(obj).lower()


def get_src_and_tgt(file: str) -> Tuple[str, str]:
    migratio = file.split('/')[-2] 
    src_app = migratio.split('-')[0]
    tgt_app = migratio.split('-')[1]
    if ALGORITHM == "craftdroid":
        src_app = src_app + migration.split('-')[2]
        tgt_app = tgt_app + migration.split('-')[2]
    return src_app, tgt_app


def add_corresponding_objects_to_map(result: pd.core.frame.DataFrame,
                                     file: str,
                                     generated: list,
                                     ground_truth: list) -> pd.core.frame.DataFrame:
    src_app, tgt_app = get_src_and_tgt(file)
    for i, gt in enumerate(ground_truth):
        gt = drop_page_bounds(gt)
        equal_gens = []
        for j, gen in enumerate(generated):
            gen = drop_page_bounds(gen)
            if ordered(gen) == ordered(gt):
                equal_gens.append(str(j))
        if len(equal_gens):
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
            config[ALGORITHM]['BASE_JSON_ADDRESS']['address'] + "generated/" + migration_config + "/*/*_final.json")
        extract_ground_truth_generated_map(files, migration_config)


def main():
    extract_all_ground_truth_generated_maps()


if __name__ == '__main__':
    main()
