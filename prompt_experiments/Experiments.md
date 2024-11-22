## Experiment 1: Trivial Prompt

Result data in `single_agent_trivial_prompt/`

This experiment uses a simple prompt to test Llama-3's general capability in summarizing legal documents.

__Observation:__
- 8b model is performs poorly; it even hallucinates and generate made-up facts.
- 70b model performs great. It's generation is even comparable with that from GPT-4o

__Conclusion:__ We should use 70b model, not 8b model, as it does not seem to have the capability of summarizing large text.

## Experiment 2: Longer, More Complicated Prompt

Result data in `single_agent_longer_prompt_1` and `single_agent_longer_prompt_2`

This experiment uses longer prompts with more instructions to generate our intended output.

__Observation:__
- 8b still performs poorly as expected.
- 70b is generating slightly better results but not exactly satisfies the requirements.
- 70b starts to perform worse than GPT-4o

__Conclusion:__ We need to adjust the prompt and architecture more carefully for 70b

## Experiment 3: Multi-agent Architecture

Result data for multi-agent in `multi_agent_concat_results/`

This experiment explores the multi-agent architecture by summarizing facts, procedural history, and reasonings separately using different prompts, and then we concatenate the results together to form the final result.

As a comparison, we also create a single agent that combines each prompt from multi-agent to generate the summary, and the result is obviously worse than that of multi-agent. The result data for this single agent experiment is in `single_agent_multi_task/`

__Observation:__
- The quality of the summary improves significantly, qualitatively and quantitatively (in terms of comparison scores).
- It seems that 70b model is not good at handle multiple tasks in a single prompt according to the single agent multi-task experiment.
- The 70b model doesn't seem to always pay attention to the details in the prompt, like how many paragraphs should the output be.
- 70b model also tends to include the prompt's instruction again in the generated output, which is unwanted for our project.

__Conclusion:__ We should use multi-agent architecture, and the prompt for 70b model should be straightforward and contain less instructions.