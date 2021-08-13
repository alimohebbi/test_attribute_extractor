import toml
import pandas as pd
import mapping

with open('config.toml', 'r') as file:
        config = toml.load(file)

def get_new_mapping(src_app, target_app):
    return mapping.Mapping(
                src_app,
                target_app,
                config['sizes']['src']['size'],
                config['sizes']['gt']['size'],
                config['sizes']['gen']['size']
            )

def extract_sub_mappings(mappings, map_name):
    df = pd.read_csv(config['data'][map_name]['address'])
    for i in range(len(df)):
        mapping_id = mapping.Mapping.id(df['src_app'][i], df['target_app'][i])
        if mapping_id not in mappings:
            mappings[mapping_id] = get_new_mapping(df['src_app'][i], df['target_app'][i])        
        if map_name == "src_gt":
            mappings[mapping_id].add_src_gt(df['src_index'][i], df['target_index'][i])
        elif map_name == "gt_gen":
            mappings[mapping_id].add_gt_gen(df['src_index'][i], df['target_index'][i])
    return mappings

def extract_mappings():
    mappings = extract_sub_mappings(dict(), "src_gt")
    mappings = extract_sub_mappings(mappings, "gt_gen")
    for m in mappings.values():
        m.extract_one_to_one_gt_gen()
    return mappings

def calculate_metrics(migration):
    tp = migration.true_positive()
    tn = migration.true_negative()
    fp = migration.false_positive()
    fn = migration.false_negative()
    effort = migration.levenshtein_distance()
    try:
        accuracy = (tp + tn) / (tp + fp + fn + tn)
    except ZeroDivisionError:
        accuracy = None
    try:
        precision = tp / (tp + fp)
    except ZeroDivisionError:
        precision = None
    try:
        recall = tp / (tp + fn)
    except ZeroDivisionError:
        recall = None
    try:
        f1_score = 2 * (recall * precision) / (recall + precision)
    except ZeroDivisionError:
        f1_score = None
    try:
        reduction = (migration.gt_size - effort) / migration.gt_size
    except ZeroDivisionError:
        reduction = None
    return [ migration.src_app, migration.tgt_app, tp, tn, fp, fn, effort, accuracy, precision, recall, f1_score, reduction ]

def calculate_results(mappings):
    columns=["src_app", "target_app", "tp", "tn", "fp", "fn", "effort", "accuracy", "precision", "recall", "f1_score", "reduction"]
    results = []
    for k, v in mappings.items():
        if len(v.gt_gen):
            results.append(calculate_metrics(v))
    pd.DataFrame(results, columns=columns).to_csv(config['data']['result']['address'], index=False)
    print(pd.DataFrame(results, columns=columns))

def main():
    mappings = extract_mappings()
    calculate_results(mappings)
    
if __name__ == '__main__':
    main()