---
name: search-grounding
description: Real-time Google Search grounding, live web query integration, and web source citation extraction.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Google Search Grounding Skill

## Overview
This skill implements real-time Search Grounding using Google Search. When enabled, Gemini dynamically queries the live web to retrieve current information, ground its answers in factual web search results, and return source URLs (citations) with inline metadata.

---

## When to Use This Skill
- Asking about current events, breaking news, or live sports scores.
- Checking stock prices, weather updates, or recently published papers.
- Grounding factual queries to minimize hallucinations.
- Automatically showing verified reference links to users.

---

## Quick Start (with runnable code examples)

```python
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

def query_grounded_web(prompt: str):
    print(f"Querying Gemini with Search Grounding: '{prompt}'...")
    
    # Run content generation with google_search tool enabled
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=dict(
            # Enable the Google Search tool
            tools=[{'google_search': {}}]
        )
    )
    
    print("\n--- Grounded Answer ---")
    print(response.text)
    
    # Extract Search Sources and Grounding Metadata
    metadata = response.candidates[0].grounding_metadata
    if metadata and metadata.grounding_chunks:
        print("\n--- Sources Used ---")
        for i, chunk in enumerate(metadata.grounding_chunks, 1):
            web_info = chunk.web
            if web_info:
                print(f"[{i}] {web_info.title}")
                print(f"    URL: {web_info.uri}")
                
        # Print web search queries Gemini actually executed
        if metadata.web_search_queries:
            print(f"\nExecuted Queries: {', '.join(metadata.web_search_queries)}")
    else:
        print("\nNo search grounding chunks used.")

if __name__ == "__main__":
    query_grounded_web("What is the current stock price of Google, and what are the major news drivers today?")
```

---

## Advanced Usage

### Customizing Search Grounding Configurations
You can verify and map the search queries that the model executes or use the metadata to show inline hyperlinks in chat interfaces:

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Tell me who won the latest Formula 1 Grand Prix",
    config=dict(
        tools=[{'google_search': {}}]
    )
)

metadata = response.candidates[0].grounding_metadata
# Accessing supporting passage parts mapping to the sources
if metadata.search_entry_point:
    print("Render HTML query snippets:")
    print(metadata.search_entry_point.rendered_content_html)
```

---

## Key References
- [Google GenAI Search Grounding Reference](https://github.com/googleapis/python-genai)
- Gemini Grounding Guide

---

## Dependencies
- `google-genai>=0.1.1`
