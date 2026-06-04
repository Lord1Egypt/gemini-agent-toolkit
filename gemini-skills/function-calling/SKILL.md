---
name: function-calling
description: Registering custom Python tools, handling parallel function calls, and executing callback routines.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Gemini Function Calling & Tool Integration Skill

## Overview
This skill describes how to connect Gemini models to external tool APIs. By declaring Python functions as tools, the model returns structured tool call instructions when it needs to retrieve live data, execute calculations, or write data. The calling application executes the actual code and returns the output to Gemini to compile a final answer.

---

## When to Use This Skill
- Fetching live info from databases, web endpoints, or hardware sensors.
- Performing strict computations (e.g. currency conversion, SQL executions).
- Connecting agent workflows to system commands or external systems (like sending slack alerts or Telegram updates).

---

## Quick Start (with runnable code examples)

```python
import json
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

# 1. Define the actual tool functions in Python
def fetch_weather(location: str) -> str:
    """Retrieve the current weather status for a given city location.
    
    Args:
        location: The name of the city (e.g., Cairo, London, Tokyo)
    """
    # Simulate a database check or API call
    db = {
        "cairo": "Sunny and hot, 38°C",
        "london": "Overcast and rainy, 14°C",
        "tokyo": "Mild and humid, 22°C"
    }
    loc = location.strip().lower()
    return db.get(loc, f"Moderate and clear, 20°C in {location}")

def calculate_tax(amount: float, rate: float = 0.14) -> float:
    """Calculate the tax amount for a transaction.
    
    Args:
        amount: The base transaction money amount
        rate: The tax rate percentage decimal (default is 0.14 for 14%)
    """
    return round(amount * rate, 2)

# 2. Run the tool loop
def run_tool_use_agent(user_query: str):
    print(f"User Request: '{user_query}'")
    
    # Send functions to model as tools (Gemini reads the docstrings/types)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_query,
        config=dict(
            tools=[fetch_weather, calculate_tax]
        )
    )
    
    # Check if the model wants to execute a function call
    function_calls = response.function_calls
    if function_calls:
        print("\n--- Gemini Requested Function Calls ---")
        history = [response.candidates[0].content]
        
        # Process each requested function call
        for call in function_calls:
            name = call.name
            args = call.args
            print(f"Executing local function '{name}' with arguments: {args}")
            
            # Route and execute locally
            if name == "fetch_weather":
                result = fetch_weather(**args)
            elif name == "calculate_tax":
                result = calculate_tax(**args)
            else:
                result = "Error: Tool not found"
                
            print(f"Result: {result}")
            
            # Append the function call result back as a tool response
            history.append({
                "role": "tool",
                "parts": [{
                    "function_response": {
                        "name": name,
                        "response": {"result": result}
                    }
                }]
            })
            
        # Send the execution history back to Gemini to generate the final text reply
        final_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=history,
            config=dict(
                tools=[fetch_weather, calculate_tax]
            )
        )
        print("\n--- Final Grounded Output ---")
        print(final_response.text)
    else:
        print("\nGemini did not require any function calls.")
        print(response.text)

if __name__ == "__main__":
    run_tool_use_agent("I need the weather in Cairo, and please calculate the 14% tax on a $250 invoice.")
```

---

## Advanced Usage

### Forcing Specific Modes (Function Calling Constraints)
You can force Gemini to call a specific function, or run purely in text mode without using tools:

```python
# Force the model to choose from tools and output a function call
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Analyze cairo",
    config=dict(
        tools=[fetch_weather],
        tool_config={
            "function_calling_config": {
                "mode": "ANY" # Options: AUTO, ANY, NONE
            }
        }
    )
)
```

---

## Key References
- [Google GenAI Function Calling API docs](https://github.com/googleapis/python-genai)
- Gemini Function Calling Guide

---

## Dependencies
- `google-genai>=0.1.1`
