---
name: code-execution
description: Enabling Gemini's native sandboxed Python runtime, capturing code outputs, and mathematical/scientific executions.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Gemini Code Execution Skill

## Overview
This skill outlines how to enable Gemini's native, sandboxed **Python Code Execution** environment. When activated, Gemini can write Python code, execute it in an isolated sandbox during the generation process, inspect the printed outputs, and use the results to build its final answer.

---

## When to Use This Skill
- Complex mathematical equations or calculations.
- Data analysis on provided charts or tables (e.g. calculating standard deviations, regressions).
- Algorithms, code generation testing, and logic verifications.

---

## Quick Start (with runnable code examples)

```python
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

def run_scientific_computation(prompt: str):
    print(f"Sending prompt to Gemini with Native Python Execution: '{prompt}'...")
    
    # Configure the generate_content call with code_execution tool
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=dict(
            # Enable native code execution environment
            tools=[{'code_execution': {}}]
        )
    )
    
    print("\n--- Final Text Output ---")
    print(response.text)
    
    # Inspect the code that Gemini wrote and executed in the background
    candidate = response.candidates[0]
    parts = candidate.content.parts
    
    print("\n--- Background Code Executions ---")
    for part in parts:
        if part.function_call and part.function_call.name == "_exec_code":
            print("\n>>> Code Written by Gemini:")
            print(part.function_call.args.get("code"))
        elif part.function_response and part.function_response.name == "_exec_code":
            print("\n<<< Sandbox Output Result:")
            print(part.function_response.response.get("result"))

if __name__ == "__main__":
    query = (
        "Find the sum of all prime numbers between 1 and 1000. "
        "Write a Python script to calculate this, execute it, and give me the result."
    )
    run_scientific_computation(query)
```

---

## Advanced Usage

### Sandbox Limitations
The code execution environment is a locked-down, transient sandbox:
- **No Internet Access**: The code inside the sandbox cannot query outside network APIs.
- **Limited Libraries**: Major preloaded packages include standard library modules, `numpy`, `scipy`, `pandas`, and `matplotlib`.
- **Ephemeral Storage**: Files written during the sandbox run are discarded immediately after the request finishes.

---

## Key References
- [Google GenAI Code Execution reference](https://github.com/googleapis/python-genai)
- Gemini Capabilities: Python Sandbox Guide

---

## Dependencies
- `google-genai>=0.1.1`
