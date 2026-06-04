---
name: structured-output
description: Structured data extraction using Pydantic schemas, strict JSON output formats, and schema validation.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Gemini Structured Output & Schema Validation Skill

## Overview
This skill provides guidelines and code patterns for enforcing structured, type-safe output formats (specifically JSON) from Gemini models. By declaring a Pydantic model or defining a JSON Schema, developers guarantee that the model's response adheres strictly to the schema structure, avoiding parsing failures at runtime.

---

## When to Use This Skill
- Extracting entities, metrics, or relationships from unstructured text.
- Generating forms, configurations, or structured databases.
- Creating API payloads or feeding downstream programming workflows.
- Classifying inputs into predefined categories.

---

## Quick Start (with runnable code examples)

```python
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

# Define the target structure using Pydantic
class EntityExtraction(BaseModel):
    name: str = Field(description="Name of the person, company, or concept")
    category: str = Field(description="Type of entity (e.g., Person, Organization, Location, Technology)")
    relevance_score: float = Field(description="Relevance score from 0.0 to 1.0")
    context_snippet: Optional[str] = Field(None, description="A snippet from the text showing where this was found")

class TextAnalysisReport(BaseModel):
    summary: str = Field(description="A concise summary of the analyzed text")
    sentiment: str = Field(description="Sentiment classification: POSITIVE, NEGATIVE, or NEUTRAL")
    entities: List[EntityExtraction] = Field(default=[], description="List of extracted entities")

def extract_structured_data(text: str):
    print("Sending text to Gemini for structured analysis...")
    
    # Generate content using gemini-2.5-flash with a schema configuration
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Analyze the following text and extract details:\n\n{text}",
        config=dict(
            # Force JSON mime type output
            response_mime_type="application/json",
            # Pass the Pydantic class to define the target schema structure
            response_schema=TextAnalysisReport
        )
    )
    
    # Parse the response text directly as a Pydantic model instance
    try:
        report = TextAnalysisReport.model_validate_json(response.text)
        print("\n--- Successfully Extracted Pydantic Object ---")
        print(f"Sentiment: {report.sentiment}")
        print(f"Summary: {report.summary}")
        print("\nEntities Found:")
        for entity in report.entities:
            print(f" - [{entity.category}] {entity.name} (Relevance: {entity.relevance_score})")
    except Exception as e:
        print(f"Failed to validate JSON output: {e}")
        print(response.text)

if __name__ == "__main__":
    sample_text = (
        "Yesterday, Google announced the release of Gemini 2.5 on their official blog in California. "
        "Sundar Pichai expressed great excitement about the natively multimodal architecture, which shows "
        "unprecedented speed improvements for developers worldwide."
    )
    extract_structured_data(sample_text)
```

---

## Advanced Usage

### Raw Dict / JSON Schema Fallback
If you are not using Pydantic, you can pass a raw dictionary containing a standard OpenAPI 3.0 schema:

```python
raw_schema = {
    "type": "OBJECT",
    "properties": {
        "items": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        }
    },
    "required": ["items"]
}

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="List five colors",
    config=dict(
        response_mime_type="application/json",
        response_schema=raw_schema
    )
)
```

---

## Key References
- [Google GenAI Structured Output documentation](https://github.com/googleapis/python-genai)
- Pydantic v2 Documentation

---

## Dependencies
- `google-genai>=0.1.1`
- `pydantic>=2.0`
