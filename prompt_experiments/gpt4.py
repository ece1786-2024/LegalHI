from openai import OpenAI

def gpt4o_api(prompt, input_file, output_file):
    
    client = OpenAI()

    input_text = None

    with open(input_file, "r") as file:
        input_text = file.read()

    llm_input = f"{prompt}\n\n{input_text}"
    response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": llm_input
                        }
                    ]
                    }
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "text"
                }
            )
    llm_output = response.choices[0].message.content
    # print(llm_output)

    with open(output_file, "w") as file:
        file.write(llm_output)