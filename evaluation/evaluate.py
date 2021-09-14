from typing import Tuple
import toml
import pandas as pd
import glob
import json
import mapping

with open('config.toml', 'r') as file:
        config = toml.load(file)

def get_file_size(base_address: str) -> int:
    address_list = glob.glob(base_address)
    if len(address_list):
        with open(address_list[0], 'r') as f:
            obj = json.load(f)
    if len(address_list) == 0 or obj is None:
        return 0
    else:
        return len(obj)

def get_file_sizes(src_app: str, target_app: str, migration_config: str) -> Tuple[int, int, int]:
    BASE_JSON_ADDRESS = config['data']['BASE_JSON_ADDRESS']['address']

    source_address = BASE_JSON_ADDRESS+"donor/"+src_app+"/*.json"
    src_size = get_file_size(source_address)

    ground_truth_address = BASE_JSON_ADDRESS+"ground_truth/"+src_app+"/"+src_app+"-"+target_app+"_attributes.json"
    gt_size = get_file_size(ground_truth_address)

    generated_address = migration_config+"/"+src_app+"-"+target_app+"/*.json"
    gen_size = get_file_size(generated_address)
    return src_size, gt_size, gen_size

def get_new_mapping(src_app: str, target_app: str, migration_config: str) -> mapping.Mapping:
    src_size, gt_size, gen_size = get_file_sizes(src_app, target_app, migration_config)
    return mapping.Mapping(src_app, target_app, src_size, gt_size, gen_size)

def extract_sub_mappings(mappings: dict, map_name: str, migration_config: str) -> dict:
    if map_name == "src_gt":
        df = pd.read_csv(config['data'][map_name]['address'])
    else:
        df = pd.read_csv(config['data'][map_name]['address']+migration_config.split("/")[-1]+".csv")
    for i in range(len(df)):
        mapping_id = mapping.Mapping.id(df['src_app'][i], df['target_app'][i])
        if mapping_id not in mappings:
            mappings[mapping_id] = get_new_mapping(df['src_app'][i], df['target_app'][i], migration_config)        
        if map_name == "src_gt":
            mappings[mapping_id].add_src_gt(df['src_index'][i], df['target_index'][i])
        elif map_name == "gt_gen":
            mappings[mapping_id].add_gt_gen(df['src_index'][i], df['target_index'][i])
    return mappings

def extract_mappings(migration_config: str) -> dict:
    mappings = extract_sub_mappings(dict(), "src_gt", migration_config)
    mappings = extract_sub_mappings(mappings, "gt_gen", migration_config)
    for m in mappings.values():
        m.extract_one_to_one_gt_gen()
    return mappings

def calculate_metrics(migration: mapping.Mapping) -> list:
    tp = migration.true_positive()
    tn = migration.true_negative()
    fp = migration.false_positive()
    fn = migration.false_negative()
    effort = migration.levenshtein_distance()
    try:
        accuracy = (tp + tn) / (tp + fp + fn + tn)
    except:
        accuracy = None
    try:
        precision = tp / (tp + fp)
    except:
        precision = None

    try:
        recall = tp / (tp + fn)
    except:
        recall = None
    try:
        f1_score = 2 * (recall * precision) / (recall + precision)
    except:
        f1_score = None
    try:
        reduction = (migration.gt_size - effort) / migration.gt_size
    except:
        reduction = None
    return [ migration.src_app, migration.tgt_app, tp, tn, fp, fn, effort, accuracy, precision, recall, f1_score, reduction ]

def calculate_results(mappings: dict, migration_config: str) -> pd.core.frame.DataFrame:
    columns=["src_app", "target_app", "tp", "tn", "fp", "fn", "effort", "accuracy", "precision", "recall", "f1_score", "reduction"]
    results = []
    for k, v in mappings.items():
        if len(v.gt_gen):
            results.append(calculate_metrics(v))
    pd.DataFrame(results, columns=columns).to_csv(config['data']['result']['address']+migration_config.split("/")[-1]+".csv", index=False)
    print(pd.DataFrame(results, columns=columns))

def main():
    migration_configs = glob.glob(config['data']['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        mappings = extract_mappings(migration_config)
        calculate_results(mappings, migration_config)
    
if __name__ == '__main__':
    main()