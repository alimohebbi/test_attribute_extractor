import toml
import pandas as pd
import mapping


def main():
    with open('config.toml', 'r') as file:
        config = toml.load(file)

    # read src gt pairs
    src_gt = pd.read_csv(config['data']['src_gt']['address'])

    # extract src gt mappings
    mappings = dict()
    for i in range(len(src_gt)):
        mapping_id = mapping.Mapping.id(src_gt['src_app'][i], src_gt['target_app'][i])
        if mapping_id not in mappings:
            mappings[mapping_id] = mapping.Mapping(
                src_gt['src_app'][i],
                src_gt['target_app'][i],
                config['sizes']['src']['size'],
                config['sizes']['gt']['size'],
                config['sizes']['gen']['size']
            )
        mappings[mapping_id].add_src_gt(src_gt['src_index'][i], src_gt['target_index'][i])

    # read gt gen pairs
    gt_gen = pd.read_csv(config['data']['gt_gen']['address'])

    # extract gt gen mappings
    for i in range(len(gt_gen)):
        mapping_id = mapping.Mapping.id(gt_gen['src_app'][i], gt_gen['target_app'][i])
        if mapping_id not in mappings:
            mappings[mapping_id] = mapping.Mapping(
                gt_gen['src_app'][i],
                gt_gen['target_app'][i],
                config['sizes']['src']['size'],
                config['sizes']['gt']['size'],
                config['sizes']['gen']['size']
            )
        mappings[mapping_id].add_gt_gen(gt_gen['src_index'][i], gt_gen['target_index'][i])

    for m in mappings.values():
        m.extract_one_to_one_gt_gen()

    result = pd.DataFrame(columns=(
        "src_app",
        "target_app",
        "tp", "tn", "fp", "fn",
        "effort",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "reduction"
    ))
    i = 0
    for elem in mappings.values():
        tp = elem.true_positive()
        tn = elem.true_negative()
        fp = elem.false_positive()
        fn = elem.false_negative()
        effort = elem.levenshtein_distance()
        accuracy = (tp + tn) / (tp + fp + fn + tn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1_score = 2 * (recall * precision) / (recall + precision)
        reduction = (elem.gt_size - effort) / elem.gt_size
        result.loc[i] = [
            elem.src_app,
            elem.tgt_app,
            tp,
            tn,
            fp,
            fn,
            effort,
            accuracy,
            precision,
            recall,
            f1_score,
            reduction
        ]
        i += 1
    result.to_csv(config['data']['result']['address'], index=False)
    print(result)


if __name__ == '__main__':
    main()