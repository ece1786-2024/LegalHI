from gpt_eval.gpt4_eval import gpt_eval
from score.score import calculate_bertscore, calculate_rouge

import argparse
import json
import tqdm


def main(input_filename, output_filename):
    
    dataset = json.load(open(input_filename))
    new_json = {}
    for k in tqdm.tqdm(dataset):
        instance = dataset[k]
        source = instance['original_text']
        system_output = instance['llama_summary']
        human_output = instance['original_summary']
        citation = instance['citation']

        new_json[k] = {}
        out_instance = new_json[k]
        out_instance['citation'] = citation
        out_instance['llama_summary'] = system_output

        nlp_scores = {}
        # 1. eval use traditional NLP scores
        rouge_scores = calculate_rouge(reference=human_output, generated=system_output)
        for metric, score in rouge_scores.items():
            nlp_scores[metric] = {
                "precision": score.precision,
                "recall": score.recall,
                "f1": score.fmeasure
            }
        bert_p, bert_r, bert_f1 = calculate_bertscore(reference=human_output, generated=system_output)
        nlp_scores['bert'] = {
                "precision": bert_p,
                "recall": bert_r,
                "f1": bert_f1
            }
        # 2. eval using G-EVAL
        nlp_scores['geval'] = gpt_eval(source, system_output)
        out_instance.update(nlp_scores)


    with open(output_filename, 'w') as f:
        json.dump(new_json, f, indent=4)

    

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output_filename', type=str, default='results.json')
    argparser.add_argument('--input_filename', type=str)
    args = argparser.parse_args()
    main(args.input_filename, args.output_filename)