import json
from architecture.model import legal_summary

def get_data(year):
    data_file = f"data/summaries/{year}_data.json"
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


def generate_by_year(year):
    data = get_data(year)
    generate_data = {}
    output_file = f"data/generate_summary/{year}_generate_response_legalhi.json"
    for i in data:
        generate_data[i] = {}
        citations = data[i]["citation"]
        generate_data[i]["original_text"] = data[i]["original_text"]
        print(f"Generating llama response for citation number {citations}")
        generate_data[i]["llama_summary"] = legal_summary(data[i]["original_text"])
        generate_data[i]["citation"] = data[i]["citation"]
        generate_data[i]["original_summary"] = data[i]["summary"]
        with open(output_file, "w") as f:
            json.dump(generate_data, f)

if __name__ == '__main__':
    generate_by_year(2024)