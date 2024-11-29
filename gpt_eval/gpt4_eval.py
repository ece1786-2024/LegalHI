'''
Modified from the original source code of G-Eval: https://github.com/nlpyang/geval

Reference: Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., & Zhu, C. (2023, December). G-Eval: NLG Evaluation using Gpt-4 with Better Human Alignment. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (pp. 2511-2522).
'''

import openai
import json
import argparse
import tqdm
import time
import os

def gpt_eval(source, system_output):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    eval_prompts = {
        "coherence": 
            'You will be given a court judgement document. You will then be given one summary written for this document.\n\nYour task is to rate the summary on one metric.\n\nPlease make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.\n\nEvaluation Criteria:\n\nCoherence (1-5) - the collective quality of all sentences. We align this dimension with the DUC quality question of structure and coherence whereby "the summary should be well-structured and well-organized. The summary should not just be a heap of related information, but should build from sentence to a coherent body of information about a topic."\n\nEvaluation Steps:\n\n1. Read the news article carefully and identify the main topic and key points.\n2. Read the summary and compare it to the news article. Check if the summary covers the main topic and key points of the news article, and if it presents them in a clear and logical order.\n3. Assign a score for coherence on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.\n\n\nExample:\n\n\nSource Text:\n\n{{Document}}\n\nSummary:\n\n{{Summary}}\n\n\nONLY output the score, nothing else.',
        "consistency": 
            "You will be given a court judgement document. You will then be given one summary written for this document.\n\nYour task is to rate the summary on one metric.\n\nPlease make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.\n\n\nEvaluation Criteria:\n\nConsistency (1-5) - the factual alignment between the summary and the summarized source. A factually consistent summary contains only statements that are entailed by the source document. Annotators were also asked to penalize summaries that contained hallucinated facts. \n\nEvaluation Steps:\n\n1. Read the news article carefully and identify the main facts and details it presents.\n2. Read the summary and compare it to the article. Check if the summary contains any factual errors that are not supported by the article.\n3. Assign a score for consistency based on the Evaluation Criteria.\n\n\nExample:\n\n\nSource Text: \n\n{{Document}}\n\nSummary: \n\n{{Summary}}\n\n\nONLY output the score, nothing else.",
        "fluency": 
            "You will be given one summary written for a court judgement.\n\nYour task is to rate the summary on one metric.\n\nPlease make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.\n\n\nEvaluation Criteria:\n\nFluency (1-3): the quality of the summary in terms of grammar, spelling, punctuation, word choice, and sentence structure.\n\n- 1: Poor. The summary has many errors that make it hard to understand or sound unnatural.\n- 2: Fair. The summary has some errors that affect the clarity or smoothness of the text, but the main points are still comprehensible.\n- 3: Good. The summary has few or no errors and is easy to read and follow.\n\n\nExample:\n\nSummary:\n\n{{Summary}}\n\n\nONLY output the score, nothing else.",
        "relevance": 
            "You will be given a court judgement document. You will then be given one summary written for this document.\n\nYour task is to rate the summary on one metric.\n\nPlease make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.\n\nEvaluation Criteria:\n\nRelevance (1-5) - selection of important content from the source. The summary should include only important information from the source document. Annotators were instructed to penalize summaries which contained redundancies and excess information.\n\nEvaluation Steps:\n\n1. Read the summary and the source document carefully.\n2. Compare the summary to the source document and identify the main points of the article.\n3. Assess how well the summary covers the main points of the article, and how much irrelevant or redundant information it contains.\n4. Assign a relevance score from 1 to 5.\n\n\nExample:\n\n\nSource Text:\n\n{{Document}}\n\nSummary:\n\n{{Summary}}\n\n\nONLY output the score, nothing else.",
        }

    out_instance = {}

    for metric, prompt in eval_prompts.items():
            cur_prompt = prompt.replace('{{Document}}', source).replace('{{Summary}}', system_output)
            while True:
                try:
                    print(f"Running {metric}...")
                    _response = openai.chat.completions.create(
                        model='gpt-4o-mini',
                        messages=[{"role": "system", "content": cur_prompt}],
                        temperature=2,
                        max_tokens=5,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stop=None,
                        # logprobs=40,
                        n=10
                    )
                    time.sleep(0.5)

                    # Take avg of multiple rsp
                    all_responses = [_response.choices[i].message.content for i in
                                    range(len(_response.choices))]
                    # print(all_responses)
                    int_rsps = []
                    for res in all_responses:
                        # GPT responses might not always follow exact format instructed by our prompt.
                        # Sometime contains nonsense texts
                        # Disregard those responses
                        try:
                            int_rsps.append(int(res))
                        except:
                            continue

                    avg_result = sum(int_rsps) / len(int_rsps)
                    out_instance[metric] = avg_result
                    break
                except Exception as e:
                    print(e)
                    if ("limit" in str(e)):
                        time.sleep(2)
                    else:
                        break
    return out_instance


def main(input_filename, output_filename):

    summeval = json.load(open(input_filename))
    new_json = {}
    for k in tqdm.tqdm(summeval):
        if k != "4":
            continue

        instance = summeval[k]
        source = instance['original_text']
        system_output = instance['llama_summary']
        human_output = instance['original_summary']
        citation = instance['citation']

        new_json[k] = {}
        out_instance = new_json[k]
        out_instance['citation'] = citation
        out_instance['llama_summary'] = system_output

        out_instance['geval'] = gpt_eval(source, system_output)

    with open(output_filename, 'w') as f:
        json.dump(new_json, f, indent=4)


if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output_filename', type=str, default='geval.json')
    argparser.add_argument('--input_filename', type=str)
    args = argparser.parse_args()
    main(args.input_filename, args.output_filename)
    