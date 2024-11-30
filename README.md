# LegalHI

## Usage

1. Set your Llama API key (required) as environment variable, below is one way of doing that:
```
export LLAMA_API_KEY=<your api key>
```

2. If you wish to get the G-Eval scores of the generated summary, also set OpenAI API key as environment variable:
```
export OPENAI_API_KEY=<your api key>
```

3. Run the Legal HI app script to generate
```
python legalhi_app.py <your input document as .txt file>
```

## Examples

prompt_experiments/example_input.tx: from https://www.canlii.org/en/ca/scc/doc/2024/2024scc38/2024scc38.html

prompt_experiments/example_truth.txt: from https://www.scc-csc.ca/case-dossier/cb/2024/40749-eng.aspx
