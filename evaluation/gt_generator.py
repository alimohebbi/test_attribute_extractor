from typing import List, Dict
import toml
import json
import glob
import pandas as pd

with open('config.toml', 'r') as file:
        config = toml.load(file)

def find_ground_truth(filename):
    filename = filename.split('/')[-2] + "_attributes.json"
    files = glob.glob(config['data']['GROUND_TRUTH_GLOBE']['address'])
    for file in files:
        if filename in file:
            return file
    return None

def load_json_files(file, gt_file_address):
    generated: List[Dict[str, object]] = None
    with open(file, 'r') as f:
            generated = json.load(f)

    ground_truth: List[Dict[str, object]] = None
    with open(gt_file_address, 'r') as f:
            ground_truth = json.load(f)

    return generated, ground_truth

def drop_page_bounds(obj):
    try:
        obj.pop('page')
    except KeyError:
        pass
    try:
        obj.pop('bounds')
    except KeyError:
        pass
    return obj

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return [ordered(x) for x in obj]
    else:
        return obj

def get_src_and_tgt(file):
    src_app =  file.split('/')[-2].split('-')[0]
    tgt_app =  file.split('/')[-2].split('-')[1]
    return src_app, tgt_app

def add_corresponding_objects_to_map(result, file, generated, ground_truth):
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

def main():
    files = glob.glob(config['data']['GENERATED_GLOBE']['address'])
    result = pd.DataFrame(columns=['src_app', 'target_app', 'src_index', 'target_index'])
    for file in files:

        gt_file_address = find_ground_truth(file)
        if gt_file_address is None:
            continue

        generated, ground_truth = load_json_files(file, gt_file_address)
        if generated is None or ground_truth is None:
            continue

        result = add_corresponding_objects_to_map(result, file, generated, ground_truth)
        
    result.to_csv(config['data']['gt_gen']['address'], index=False)


if __name__ == '__main__':
    main()