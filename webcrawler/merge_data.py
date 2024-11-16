import json
import pandas as pd

file_summary = "scc_summary_total.csv"
file_original = "original_text.json"
output_file = "final_data_first_half.json"

# first half:
df_summary = pd.read_csv(file_summary)
df_summary_first_half = df_summary[:123]


# read original txt:
with open(file_original, "r") as file:
    data = json.load(file)

# Convert JSON data to a pandas DataFrame
df_original_first_half = pd.DataFrame.from_dict(data, orient='index')

# merge them on citation:
merged_df_first_half = pd.merge(df_summary_first_half, df_original_first_half, on='citation', how='inner')


data = {}
for idx, row in merged_df_first_half.iterrows():
    data[idx] = {
                "original_text": row["original_text"],
                "original_key": row['original_key'],
                "citation": row["citation"],
                "summary": row["summary"],
            }
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

