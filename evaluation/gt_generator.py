from typing import List, Dict
import toml
import json
import glob
import pandas as pd

with open('config.toml', 'r') as file:
        config = toml.load(file)

GROUND_TRUTH_GLOBE = '../data/output/final/atm_tests/ground_truth/*/*.json'
GENERATED_GLOBE = '../data/output/final/atm_tests/migrated_tests/*/*.json'


def find_ground_truth(filename):
    files = glob.glob(GROUND_TRUTH_GLOBE)
    for file in files:
        if filename in file:
            return file
    return None


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return [ordered(x) for x in obj]
    else:
        return obj


def main():
    files = glob.glob(GENERATED_GLOBE)
    #print("GENERATED_GLOBE")
    #print(GENERATED_GLOBE)
    result = pd.DataFrame(columns=['src_app', 'target_app', 'src_index', 'target_index'])
    for file in files:
        filename = file.split('/')[-2] + "_attributes.json"
        gt_file_address = find_ground_truth(filename)
        if gt_file_address is None:
            continue
        filename = filename.strip("_attributes.json")
        src_app = filename.split('-')[0]
        tgt_app = filename.split('-')[1]
        generated: List[Dict[str, object]] = None
        with open(file, 'r') as f:
            generated = json.load(f)

        ground_truth: List[Dict[str, object]] = None
        with open(gt_file_address, 'r') as f:
            ground_truth = json.load(f)

        if generated is None or ground_truth is None:
            continue

        k = 0
        for i, gen in enumerate(generated):
            gen.pop('page')
            gen.pop('bounds')
            equal_gts = []
            for j, gt in enumerate(ground_truth):
                try:
                    gt.pop('page')
                except KeyError:
                    pass
                try:
                    gt.pop('bounds')
                except KeyError:
                    pass
                if ordered(gen) == ordered(gt):
                    equal_gts.append(str(j))
            if len(equal_gts):
                result.loc[k] = [
                    src_app,
                    tgt_app,
                    i,
                    ' '.join(equal_gts)
                ]
                k += 1
    result.to_csv(config['data']['gt_gen']['address'], index=False)


if __name__ == '__main__':
    main()