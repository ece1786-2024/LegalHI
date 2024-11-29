from llamaapi import LlamaAPI
import json
import os

def llama_api(prompt, text=None, input_file=None, output_file=None):

    # Initialize the SDK
    key = os.environ['LLAMA_API_KEY']
    llama = LlamaAPI(key)

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