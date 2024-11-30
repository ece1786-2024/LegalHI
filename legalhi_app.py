import argparse

from gpt_eval.gpt4_eval import gpt_eval
from data.generate_summary.generate_response import generate_response_llama

def main(args):
    in_file = args.input_filename
    out_file = args.output_filename

    with open(in_file, "r", encoding='utf-8') as f_in:
        input_text = f_in.read()
    
    print("Generating summary...")
    gen_summary = generate_response_llama(input_text)

    try:
        with open(out_file, "w") as f_out:
            f_out.write(gen_summary)
        print(f"Output as {out_file}")
        print("")
    except Exception as e:
        print(f"ERROR: {e}")
        print("An error has occurred. Below is the generated summary:")
        print(gen_summary)
        return

    if args.do_geval:
        print("Evaluating with GPT-4...")
        geval_score = gpt_eval(source=input_text, system_output=gen_summary)
        print("==================")
        print(f"G-EVAL Score:")
        print(f"  Coherence(1-5): {geval_score['coherence']:.3f}")
        print(f"  Consistency(1-5): {geval_score['consistency']:.3f}")
        print(f"  Fluency(1-3): {geval_score['fluency']:.3f}")
        print(f"  Relevance(1-5): {geval_score['relevance']:.3f}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_filename', type=str)
    argparser.add_argument('--do_geval', action='store_true')
    argparser.add_argument('-o', '--output_filename', type=str, default='LegalHI_summary.txt')
    args = argparser.parse_args()
    main(args)
