from typing import List, Dict, Tuple
import toml
import pandas as pd
import glob
import json
import mapping
from Levenshtein import distance
from fastDamerauLevenshtein import damerauLevenshtein


with open('../config_template/config.toml', 'r') as file:
        config = toml.load(file)
ALGORITHM = str(config["algorithm"])


def prune_df_with_oracle_pass(target_index_list, is_oracle_list, oracle_pass_list):
    new_target_index_list = []
    for i in range(len(is_oracle_list)):
        if is_oracle_list[i] == 1:
            new_matched_targets = []
            matched_targets = str(target_index_list[i]).split(" ")
            matched_oracle_pass_list = str(oracle_pass_list[i]).split(" ")
            for j in range(len(matched_oracle_pass_list)):
                if matched_oracle_pass_list[j] == "nan":
                    new_target_index_list.append(' '.join(new_matched_targets))
                elif int(float(matched_oracle_pass_list[j])):
                    new_matched_targets.append(matched_targets[j])
            new_target_index_list.append(' '.join(new_matched_targets))
        else:
            new_target_index_list.append(target_index_list[i])

    return new_target_index_list


def read_gt_gen(gt_gen_address: str, consider_oracle_pass: bool):
    if not consider_oracle_pass:
        df = pd.read_csv(gt_gen_address)
    else:
        df = pd.read_csv(gt_gen_address)
        target_index_list = list(df["target_index"])
        is_oracle_list = list(df["is_oracle"])
        oracle_pass_list = list(df["oracle_pass"])
        new_target_index_list = prune_df_with_oracle_pass(target_index_list, is_oracle_list, oracle_pass_list)
        df = pd.DataFrame(list(zip(list(df["src_app"]), list(df["target_app"]), list(df["src_index"]), new_target_index_list)),
               columns =['src_app', 'target_app', 'src_index', 'target_index'])
    return df


def atm_subject(src_app):
    return src_app.startswith("a6") or src_app.startswith("a7") or src_app.startswith("a8")


def get_craftdroid_ground_truth_address(base_path, src_app, target_app):
    if atm_subject(src_app):
        return base_path+src_app.split("-")[0]+"-"+target_app+".json"
    else:
        return base_path+target_app+".json"


def empty_event(parsed_element):
    keys = parsed_element.keys()
    if "class" in keys and parsed_element["class"] == "EMPTY_EVENT":
        return True
    return False


def remove_extra_events(obj: List[Dict[str, object]]) -> List[Dict[str, object]]:  
    obj = [x for x in obj if not empty_event(x)]
    # obj = [x for x in obj if not x["action"][0].startswith("wait") and not x["action"][0] == "KEY_BACK"]
    return obj


def get_file_size(base_address: str) -> int:
    address_list = glob.glob(base_address)
    if len(address_list):
        with open(address_list[0], 'r') as f:
            obj = json.load(f)
    if len(address_list) == 0 or obj is None:
        return 0
    else:
        obj = remove_extra_events(obj)
        return len(obj)


def get_file_addresses(src_app: str, target_app: str, migration_config: str) -> Tuple[str, str, str]:
    BASE_JSON_ADDRESS = config[ALGORITHM]['BASE_JSON_ADDRESS']['address']
    if ALGORITHM == "atm":
        source_address = BASE_JSON_ADDRESS+"donor/"+src_app+"/*.json"
        ground_truth_address = BASE_JSON_ADDRESS+"ground_truth/"+src_app+"/"+src_app+"-"+target_app+"_attributes.json"
        generated_address = BASE_JSON_ADDRESS+"generated/"+migration_config.split("/")[-1]+"/"+src_app+"-"+target_app+"/*.json"
    else:
        source_address = BASE_JSON_ADDRESS+"donor/"+src_app+"*.json"
        ground_truth_address = get_craftdroid_ground_truth_address(BASE_JSON_ADDRESS+"ground_truth/", src_app, target_app)
        generated_address = BASE_JSON_ADDRESS+"generated/"+migration_config.split("/")[-1]+"/"+src_app.split("-")[0]+"-"+target_app+"/*.json"
    return source_address, ground_truth_address, generated_address


def get_file_sizes(src_app: str, target_app: str, migration_config: str) -> Tuple[int, int, int]:
    source_address, ground_truth_address, generated_address = get_file_addresses(src_app, target_app, migration_config)
    src_size = get_file_size(source_address)
    gt_size = get_file_size(ground_truth_address)
    gen_size = get_file_size(generated_address)
    return src_size, gt_size, gen_size


def get_new_mapping(src_app: str, target_app: str, migration_config: str) -> mapping.Mapping:
    src_size, gt_size, gen_size = get_file_sizes(src_app, target_app, migration_config)
    return mapping.Mapping(src_app, target_app, src_size, gt_size, gen_size)


def extract_sub_mappings(mappings: dict, map_name: str, migration_config: str, oracle_stat: str, consider_oracle_pass: bool) -> dict:
    if map_name == "src_gt":
        df = pd.read_csv(config[ALGORITHM][map_name][oracle_stat])
    else:
        gt_gen_address = config[ALGORITHM][map_name]['address']+oracle_stat+"/"+migration_config.split("/")[-1]+".csv"
        df = read_gt_gen(gt_gen_address, consider_oracle_pass)
    for i in range(len(df)):
        mapping_id = mapping.Mapping.id(df['src_app'][i], df['target_app'][i])
        if mapping_id not in mappings:
            mappings[mapping_id] = get_new_mapping(df['src_app'][i], df['target_app'][i], migration_config)        
        if map_name == "src_gt":
            mappings[mapping_id].add_src_gt(df['src_index'][i], df['target_index'][i])
        elif map_name == "gt_gen":
            mappings[mapping_id].add_gt_gen(df['src_index'][i], df['target_index'][i])
    return mappings


def extract_mappings(migration_config: str, oracle_stat: str, consider_oracle_pass = False) -> dict:
    mappings = extract_sub_mappings(dict(), "src_gt", migration_config, oracle_stat, consider_oracle_pass)
    mappings = extract_sub_mappings(mappings, "gt_gen", migration_config, oracle_stat, consider_oracle_pass)
    for m in mappings.values():
        m.extract_one_to_one_gt_gen()
    return mappings


def calculate_metrics(migration: mapping.Mapping) -> list:
    tp = migration.true_positive()
    tn = migration.true_negative()
    fp = migration.false_positive()
    fn = migration.false_negative()
    
    gt_str, gen_str = migration.build_distance_strings()
    if gt_str is None or gen_str is None:
        effort_leveneshtein = None
        effort_damerau_levenshtein = None
    else:
        effort_leveneshtein = distance(gt_str, gen_str)
        effort_damerau_levenshtein = int(damerauLevenshtein(gt_str, gen_str, similarity=False))

    try:
        accuracy = (tp + tn) / (tp + fp + fn + tn)
    except Exception as e:
        accuracy = None

    try:
        precision = tp / (tp + fp)
    except Exception as e:
        precision = None

    try:
        recall = tp / (tp + fn)
    except Exception as e:
        recall = None

    try:
        f1_score = 2 * (recall * precision) / (recall + precision)
    except Exception as e:
        f1_score = None

    try:
        reduction_leveneshtein = (migration.gt_size - effort_leveneshtein) / migration.gt_size
    except Exception as e:
        reduction_leveneshtein = None

    try:
        reduction_damerau_leveneshtein = (migration.gt_size - effort_damerau_levenshtein) / migration.gt_size
    except Exception as e:
        reduction_damerau_leveneshtein = None

    return [ migration.src_app, migration.tgt_app, tp, tn, fp, fn,\
    effort_leveneshtein, effort_damerau_levenshtein, accuracy, precision,\
    recall, f1_score, reduction_leveneshtein, reduction_damerau_leveneshtein ]


def calculate_results(mappings: dict, result_address: str) -> pd.core.frame.DataFrame:
    columns=["src_app", "target_app", "tp", "tn", "fp", "fn", "effort_leveneshtein",\
    "effort_damerau_levenshtein", "accuracy", "precision", "recall", "f1_score",\
    "reduction_leveneshtein", "reduction_damerau_leveneshtein"]
    results = []
    for k, v in mappings.items():
        if len(v.gt_gen):
            results.append(calculate_metrics(v))
    pd.DataFrame(results, columns=columns).to_csv(result_address, index=False)
    print(pd.DataFrame(results, columns=columns))


def get_result_address(oracle_stat: str, file_name:str, consider_oracle_pass = False):
    if oracle_stat == "oracles_excluded":
        result_address = config[ALGORITHM]['result'][oracle_stat]+file_name
    else:
        if consider_oracle_pass:
            result_address = config[ALGORITHM]['result'][oracle_stat]+"with_oracle_pass/"+file_name
        else:
            result_address = config[ALGORITHM]['result'][oracle_stat]+"without_oracle_pass/"+file_name
    return result_address


def evaluate_oracle_stats(migration_config: str):
    file_name = "result_" + migration_config.split("/")[-1]+".csv"
    
    for oracle_stat in ["oracles_excluded", "oracles_included", "oracles_only"]:
        if oracle_stat == "oracles_excluded":
            mappings = extract_mappings(migration_config, oracle_stat)
            result_address = get_result_address(oracle_stat, file_name)
            calculate_results(mappings, result_address)
        else:
            for consider_oracle_pass in [0, 1]:
                mappings = extract_mappings(migration_config, oracle_stat, consider_oracle_pass)
                result_address = get_result_address(oracle_stat, file_name, consider_oracle_pass)
                calculate_results(mappings, result_address)


def evaluate_all_configs():
    migration_configs = glob.glob(config[ALGORITHM]['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        print(migration_config)
        evaluate_oracle_stats(migration_config)


def main():
    evaluate_all_configs()    
    

if __name__ == '__main__':
    main()
