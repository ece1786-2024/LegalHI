import os
import argparse
import json


def main(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
    
    baseline_avg_metrics = {}
    for metric in ['rouge1','rouge2','rougeL', 'bert']:
        for val in ['precision','recall','f1']:
            baseline_avg_metrics[f'{metric}_{val}'] = 0

    num_data = len(data)

    for k, item in data.items():
        for metric in ['rouge1','rouge2','rougeL', 'bert']:
            score = item[metric]
            for val in ['precision','recall','f1']:
                baseline_avg_metrics[f'{metric}_{val}'] += score[val]

    for metric in ['rouge1','rouge2','rougeL', 'bert']:
        for val in ['precision','recall','f1']:
            baseline_avg_metrics[f'{metric}_{val}'] /= num_data
    
    print(baseline_avg_metrics)
    print(num_data)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_filename', type=str)
    args = argparser.parse_args()
    main(args.input_filename)