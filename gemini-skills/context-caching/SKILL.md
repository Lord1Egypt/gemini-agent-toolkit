---
name: context-caching
description: Large context caching, cached token management, TTL config, and cost optimization.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Gemini Context Caching Skill

## Overview
This skill implements Gemini's native **Context Caching** API. Context Caching allows you to upload large, reusable pieces of data (e.g. video files, massive directories of text, or large PDFs) to Google's servers once, cache the parsed tokens, and query them multiple times.

Caching significantly reduces both query latency and per-request token costs when dealing with contents larger than 32,768 tokens (up to 2 million tokens).

---

## When to Use This Skill
- Building interactive developer agents that need to inspect an entire codebase continuously.
- Q&A bots querying thick books, academic corpuses, or large financial directories.
- Repetitive analysis of long videos or extensive audio recordings.
- Cost reduction for high-frequency user interactions over a stable background dataset.

---

## Quick Start (with runnable code examples)

```python
import time
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

def create_and_use_cache(document_path: str):
    print("Uploading target file for context caching...")
    doc_file = client.files.upload(file=document_path)
    
    # Wait for file to become active
    while doc_file.state.name == "PROCESSING":
        time.sleep(2)
        doc_file = client.files.get(name=doc_file.name)
        
    print(f"Creating Gemini Context Cache for: {doc_file.name}...")
    
    # Create the cache
    cache = client.caches.create(
        model='gemini-2.5-flash',
        config=dict(
            # Pass the files or text contents to cache
            contents=[doc_file],
            # Time to live (TTL) before the cache expires automatically
            ttl='300s', # 5 minutes
            # Provide a descriptive name/label for management
            display_name="large_document_reference_cache"
        )
    )
    
    print(f"Cache created successfully! Cache Name: {cache.name}")
    print(f"Expires at: {cache.expire_time}")
    
    # Query using the cached content
    print("\nQuerying Gemini using the cache token bank...")
    response1 = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Summarize Section 3 of the document.",
        config=dict(
            # Link the query to the cache resource name
            cached_content=cache.name
        )
    )
    print("Response 1:", response1.text)
    
    # Run a second query (reuses the cache, saving time and tokens)
    response2 = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Extract all dates mentioned in the text.",
        config=dict(
            cached_content=cache.name
        )
    )
    print("\nResponse 2:", response2.text)
    
    # Cleanup: Delete the cache token bank
    print("\nCleaning up cache...")
    client.caches.delete(name=cache.name)
    client.files.delete(name=doc_file.name)

if __name__ == "__main__":
    # Create a dummy file for demonstration
    with open("temp_large_doc.txt", "w") as f:
        f.write("Section 1: Intro. Section 2: General Rules. Section 3: Analysis of results from 2026-06-04.")
        
    create_and_use_cache("temp_large_doc.txt")
```

---

## Advanced Usage

### Monitoring Cache Resources & Extending TTL
You can inspect the cache size, verify token details, and update the time-to-live expiration dynamically:

```python
# Retrieve active cache information
my_cache = client.caches.get(name=cache.name)
print(f"Cached tokens count: {my_cache.metadata.total_token_count}")

# Extend cache lifetime by resetting the TTL
client.caches.patch(
    name=cache.name,
    config=dict(
        ttl='600s' # Extend by another 10 minutes
    )
)
```

---

## Key References
- [Gemini Context Caching Guide](https://github.com/googleapis/python-genai)
- Google API Pricing for Cached Tokens

---

## Dependencies
- `google-genai>=0.1.1`
