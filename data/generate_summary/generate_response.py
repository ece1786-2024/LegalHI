import json
from llamaapi import LlamaAPI

def get_data(year):
    data_file = f"C:\study\ECE1786\project\summary_files\\{year}_data.json"
    with open(data_file, "r") as f:
        data = json.load(f)
    return data


def llama_api(prompt, text=None, input_file=None, output_file=None):
    # Initialize the SDK
    str = "your_llamaApi_key"
    llama = LlamaAPI(str)
    if input_file is None:
        input_text = text
    else:
        with open(input_file, "r") as file:
            input_text = file.read()

    llm_input = f"{prompt}\n\n{input_text}"

    # Build the API request
    api_request_json = {
        "model": "llama3.1-70b",
        "messages": [
            {"role": "user", "content": llm_input},
        ],
        "max_tokens": 2048,
        # "temperature": 1.0,
        # "top_p": 1.0
    }

    # Execute the Request
    response = llama.run(api_request_json)
    rsp_dict = response.json()

    llm_output = rsp_dict['choices'][0]['message']['content']

    if output_file is not None:
        with open(output_file, "w") as file:
            file.write(llm_output)

    return llm_output


def generate_response_llama(input_text):
    agents_prompts = {
        "agent_1": (
            "Summarize the background of the case in one concise paragraph. Include the complainant, the accused, the alleged offences, and references to applicable sections of the Criminal Code."
            "Focus on the complainant, the accused, and the core allegations."
        ),
        "agent_2": (
            "Summarize the entire court proceedings in one concise paragraph, including: "
            "- The trial process: Describe the evidence presented, the trial judge's decision, and their reasoning. "
            "- The appellate process: Highlight the appellate arguments, the appellate courts' reasoning, and their decisions. "
            "- The final decision: Summarize the final judgment and reasoning of the highest court involved in this case. "
            "Focus on the logical progression of the case and key reasoning at each stage."
        ),
        "agent_3": (
            "Summarize the most critical legal principle established in this case in one concise sentence. "
            "Focus on the general relevance of the evidence, its relationship to the legal elements of the offence, and ensure the principle can apply broadly in similar cases."
        ),
        "agent_4": (
            "Write a concluding paragraph starting with 'Writing for the'. "
            "Summarize the majority opinion, focusing on the reasoning and its implications for the case."
        ),
    }
    agent_5_prompt = (
        "Combine the following text outputs from seven agents into a single cohesive and well-structured summary. "
        "Follow this structure and ensure each section adheres to the specified format: "
        "1. Title: Begin with the name of the court and provide a concise summary of the decision. For example, 'The Supreme Court sets aside...'. "
        "2. Introduction: Write one sentence starting with 'This appeal' that summarizes the central legal question. "
        "3. Background: Summarize the case facts, including the complainant, the accused, the alleged offences, and references to relevant legal provisions. "
        "4. Court Proceedings: Describe the entire court process in one paragraph, including the trial, appellate decisions, and final judgment, ensuring smooth progression. "
        "5. Legal Principle: Provide the most critical legal principle established by the court in one concise sentence. Ensure it is general and applicable to similar cases. "
        "6. Conclusion: Write a concluding paragraph starting with 'Writing for the', summarizing the court's reasoning and its broader implications for the law. "
        "- Remove all redundancy or repetition while preserving critical legal principles and facts. "
        "- Ensure smooth transitions between sections, with each part contributing to a clear and logical narrative."
        "- Part 5 should be absolutely one sentence, and not include the specific cases or facts."
        "- part 6 should not be changed too much."
    )
    generated_paragraphs = {}
    for agent_name, prompt in agents_prompts.items():
        content = llama_api(
            prompt=prompt,
            text=input_text,
        )
        generated_paragraphs[agent_name] = content
    all_paragraphs_combined = "\n\n".join(generated_paragraphs.values())
    final_output = llama_api(
        prompt=agent_5_prompt,
        text=all_paragraphs_combined,
    )
    return final_output


def generate_by_year(year):
    data = get_data(year)
    generate_data = {}
    output_file = f"{year}_generate_response.json"
    for i in data:
        generate_data[i] = {}
        citations = data[i]["citation"]
        generate_data[i]["original_text"] = data[i]["original_text"]
        print(f"Generating llama response for citation number {citations}")
        generate_data[i]["llama_summary"] = generate_response_llama(data[i]["original_text"])
        generate_data[i]["citation"] = data[i]["citation"]
        generate_data[i]["original_summary"] = data[i]["summary"]
        with open(output_file, "w") as f:
            json.dump(generate_data, f)

generate_by_year(2024)