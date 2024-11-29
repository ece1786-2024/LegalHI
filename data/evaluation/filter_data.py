import json
import re


if __name__ == "__main__":
    
    f_22 = open("..\generate_summary\\2022_generate_response.json", "r")
    f_23 = open("..\generate_summary\\2023_generate_response.json", "r")
    f_24 = open("..\generate_summary\\2024_generate_response.json", "r")

    data_22 = json.load(f_22)
    data_23 = json.load(f_23)
    data_24 = json.load(f_24)

    idx = 0
    out_data = {}
    for data_2x in [data_22, data_23, data_24]:
        for k, data in data_2x.items():
            source = data["original_text"]
            # Word count of input document
            # remove empty strings
            words = list(filter(lambda w: len(w)>0, re.split(' |\n|\t', source)))
            wc = len(words)
            # Not all documents have enough information to summarize. Here, any legal doc with less than 100 words is deemed not informative.
            if wc <= 1000:
                print(f"{data['citation']} has less than 1000 words ({wc}), discarded.")
                continue
            out_data[str(idx)] = data
            idx += 1

    with open("eval_dataset.json", "w") as f:
        json.dump(out_data, f, indent=4)

    f_22.close()
    f_23.close()
    f_24.close()

