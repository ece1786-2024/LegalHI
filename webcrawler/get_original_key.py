import pandas as pd

file = "scc_summary_total.csv"
df = pd.read_csv(file)
keys = df["citation"]
new_keys = []
for i in keys:
    if "error:" in i:
        new_key = "ERROR"
    else:
        key_split = i.split(" ")
        # in format 2024/2024scc38/2024scc38.html
        base_url = "https://www.canlii.org/en/ca/scc/doc/"
        new_key = base_url + key_split[0] + "/" + \
                    key_split[0]+ key_split[1].lower() + key_split[2]  + "/" + \
                  key_split[0] + key_split[1].lower() + key_split[2] + ".html"
    new_keys.append(new_key)
new_keys = pd.DataFrame(new_keys,columns=["keys"])
new_keys["citation"] = keys
# get the data before line 122
new_keys[123:].to_csv("original_keys.csv")