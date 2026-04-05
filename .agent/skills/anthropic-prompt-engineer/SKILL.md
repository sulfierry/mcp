---
name: anthropic-prompt-engineer
description: Oficial methodology for prompt crafting based on Anthropics research. XML tags, chain of thought, and clear system constraints.
---

# 🤖 Anthropic Prompt Engineer

This skill enforces the highest standards of prompt engineering as dictated by the Anthropics engineering team and research labs. Use this when writing instructions for LLMs, generating structured data, or configuring other agents.

## Core Directives

1. **Use XML Tags Exclusively for Structure:**
   - Always wrap content, examples, variables, and context in clear `<xml_tags>`.
   - Never use triple backticks for structural delimitation unless returning a raw code block.
   - Example: `<instructions>`, `<example_1>`, `<user_input>`.

2. **Mandatory Chain of Thought (`<thought>`):**
   - For complex tasks, you MUST instruct the target LLM to think before acting.
   - Force the model to output a `<thought>` or `<scratchpad>` block before delivering the final `<answer>`.

3. **Be Clear, Direct, and Specific:**
   - Avoid vague verbs ("Please try to make it sound professional"). 
   - Use concrete directives ("Adopt an authoritative tone, use bullet points, and limit sentences to 15 words").

4. **Provide Edge-Case Handling:**
   - Always tell the model what to do if the task fails or if the data is missing (e.g., "If the value is null, return exactly 'N/A' and do not hallucinate").

5. **Prefill the Assistant (When applicable):**
   - Suggest partial outputs to steer the model into the right format.

## Verification
When this skill is active, the agent must review any generated prompts or system instructions and score them against the 5 directives above before finalizing.
