import json
import argparse

from score.score import calculate_bertscore, calculate_rouge

from architecture.model import llama_api


def main(input_file, output_file):
    with open(input_file, "r") as f_in:
        input_json = json.load(f_in)

    output_json = {}
    for k, item in input_json.items():
        input_txt = item['original_text']

        simple_prompt = "Write a summary for the following document. The summary should include the court's decision in one sentence, the central legal question in one sentence, the background of the case in one paragraph, the court proceedings in one paragraph, the legal principle established in one sentence, and the court's reasoning in one paragraph."

        out_summary = llama_api(simple_prompt, text=input_txt)

        output_json[k] = {}
        otem = output_json[k]
        otem['citation'] = item['citation']
        otem['baseline_summary'] = out_summary
        human_output = item['original_summary']
        otem['original_summary'] = human_output

        nlp_scores = {}
        # eval use traditional NLP scores
        rouge_scores = calculate_rouge(reference=human_output, generated=out_summary)
        for metric, score in rouge_scores.items():
            nlp_scores[metric] = {
                "precision": score.precision,
                "recall": score.recall,
                "f1": score.fmeasure
            }
        bert_p, bert_r, bert_f1 = calculate_bertscore(reference=human_output, generated=out_summary)
        nlp_scores['bert'] = {
                "precision": bert_p,
                "recall": bert_r,
                "f1": bert_f1
            }

        otem.update(nlp_scores)
    
        with open(output_file, "w") as f_out:
            json.dump(output_json, f_out, indent=4)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_filename', type=str)
    argparser.add_argument('-o', '--output_filename', type=str)
    args = argparser.parse_args()
    main(args.input_filename, args.output_filename)
