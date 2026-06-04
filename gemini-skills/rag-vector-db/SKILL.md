---
name: rag-vector-db
description: Retrieval-Augmented Generation implementation using vector databases, embedding models, and query routines.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Rag Vector Db

## Overview
RAG enhances LLM outputs by retrieving relevant documents from an external vector index based on query embeddings.

## When to Use This Skill
Use to build custom Q&A pipelines over proprietary documentation files or PDF sets.

## Quick Start (with runnable code examples)

```python
# Simple cosine similarity matching using numpy (conceptual vector lookup)
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

v_query = np.array([0.1, 0.2, 0.9])
v_doc = np.array([0.11, 0.19, 0.88])
print("Match Score:", cosine_similarity(v_query, v_doc))
```

## Advanced Usage
Integrate ChromaDB/Pinecone clients, slice texts using recursive chunking algorithms, and build reranking layers.

## Key References
- [LlamaIndex Documentation](https://www.llamaindex.ai/)

## Dependencies
- numpy>=1.20.0
