import pandas as pd

files = ["scc_summary_2.csv", "scc_summary_3.csv"]

total_df = pd.read_csv("scc_summary.csv")
for i in files:
    df = pd.read_csv(i)
    total_df = pd.concat([total_df, df], ignore_index=True)  # Concatenate directly

total_df.to_csv("scc_summary_total.csv", index=False)