from llamaapi import LlamaAPI
import json

def llama_api(prompt, text=None, input_file=None, output_file=None):

    # Initialize the SDK
    llama = LlamaAPI("LA-5a3badb99f2e4bc597fe8cd06d830861f82f42ea89234908a641d4ba242ec75b")

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
    # print(llm_output)
    # ensure that LLM has completed its generation.
    assert rsp_dict['choices'][0]['finish_reason'] == 'stop'

    if output_file is not None:
        with open(output_file, "w") as file:
            file.write(llm_output)
    
    return llm_output