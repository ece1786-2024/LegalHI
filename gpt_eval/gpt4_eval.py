import openai
import json
import argparse
import tqdm
import time
import os

if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output_filename', type=str, default='geval.json')
    argparser.add_argument('--input_filename', type=str)
    # argparser.add_argument('--key', type=str, required=True)
    args = argparser.parse_args()
    openai.api_key = os.environ["OPENAI_API_KEY"]

    summeval = json.load(open(args.input_filename))
    eval_prompts = {
        "coherence": "prompts\summeval\coh_detailed.txt",
        "consistency": "prompts\summeval\con_detailed.txt",
        "fluency": "prompts\summeval\\flu_detailed.txt",
        "relevance": "prompts\summeval\\rel_detailed.txt",
        }

    ct, ignore = 0, 0

    new_json = {}
    for k in tqdm.tqdm(summeval):
        instance = summeval[k]
        source = instance['original_text']
        system_output = instance['llama_summary']
        human_output = instance['original_summary']
        citation = instance['citation']

        new_json[k] = {}
        out_instance = new_json[k]
        out_instance['citation'] = citation
        out_instance['llama_summary'] = system_output

        for metric, prompt_file in eval_prompts.items():
            prompt = open(prompt_file).read()
            cur_prompt = prompt.replace('{{Document}}', source).replace('{{Summary}}', system_output)
            # instance['prompt'] = cur_prompt
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

                    all_responses = [_response.choices[i].message.content for i in
                                    range(len(_response.choices))]
                    print(all_responses)
                    int_rsps = []
                    for res in all_responses:
                        try:
                            int_rsps.append(int(res))
                        except:
                            continue

                    avg_result = sum(int_rsps) / len(int_rsps)
                    out_instance[metric] = avg_result
                    ct += 1
                    break
                except Exception as e:
                    print(e)
                    if ("limit" in str(e)):
                        time.sleep(2)
                    else:
                        ignore += 1
                        print('ignored', ignore)
                        break


    print('ignored total', ignore)
    with open(args.output_filename, 'w') as f:
        json.dump(new_json, f, indent=4)
