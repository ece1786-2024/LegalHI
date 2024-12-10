import argparse

from architecture.model import legal_summary

def main(args):
    in_file = args.input_filename
    out_file = args.output_filename

    with open(in_file, "r", encoding='utf-8') as f_in:
        input_text = f_in.read()
    
    print("Generating summary...")
    gen_summary = legal_summary(input_text)

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

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_filename', type=str)
    argparser.add_argument('-o', '--output_filename', type=str, default='LegalHI_summary.txt')
    args = argparser.parse_args()
    main(args)
