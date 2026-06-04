<div align="center">

# 🤖 Gemini Agent Toolkit

**Structured Agentic Instructions, Skill Contexts, and SDK Integration Patterns for Gemini 2.5 Models.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Google GenAI SDK](https://img.shields.io/badge/Google--GenAI-v0.1.1+-green?logo=google&logoColor=white)](https://github.com/googleapis/python-genai)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE.md)

</div>

---

## 🚀 Overview

The **Gemini Agent Toolkit** is an open-source, production-ready framework providing **specialized operational skills** and **executable code patterns** optimized for Google's Gemini models (such as `gemini-2.5-flash` and `gemini-2.5-pro`).

Rather than relying on basic chat models, this toolkit equips developers to construct autonomous agents capable of:
1. Natively digesting complex audio & video streams.
2. Generating type-safe outputs directly mapped to Pydantic schemas.
3. Automatically querying and citing the live web via Google Search.
4. Utilizing context caches to dramatically reduce per-request token overhead.

---

## 🛠️ The 198 Agentic Skills & Domains

The toolkit contains **198 total structured skills** categorized across multiple key developer and research domains. Each skill provides a standardized, agent-parsable `SKILL.md` instruction template and copy-paste ready code examples:

### 1. 🤖 Gemini Core APIs (7 Skills)
- **`multimodal-video`**: Native video understanding and frame timelines.
- **`search-grounding`**: Real-time Google Search grounding with inline metadata source citations.
- **`structured-output`**: Defining schemas (Pydantic/JSON) for strict validation returns.
- **`context-caching`**: Reusable high-density token caching.
- **`function-calling`**: Multi-function calling triggers and callback loops.
- **`code-execution`**: Activating Gemini's native Python execution sandbox.
- **`audio-intelligence`**: Raw waveform transcriptions, speed trackers, and acoustic diagnostics.

### 2. 🌐 Web & DevOps Utilities (43 Skills)
- **Frameworks & APIs**: `fastapi-apis`, `nextjs-framework`, `express-routing`, `flask-restful-api`, `vite-frontend`.
- **Databases & ORMs**: `supabase-db`, `mongodb-db`, `sqlite-database`, `redis-caching`, `prisma-orm-db`.
- **Testing & Tooling**: `playwright-browser`, `beautifulsoup-scraping`, `python-requests-client`, `python-unittest`.
- **Infrastructure & Automation**: `github-actions-ci`, `docker-compose-utils`, `nginx-routing`, `cron-scheduling`.
- **Utilities**: `jwt-auth-utils`, `stripe-payments-api`, `cryptography-api`, `websockets-network`, `pydantic-validation`, `pydantic-settings`, `logging-monitoring`, `linux-bash-scripting`, `regular-expressions`, `semantic-versioning`, `performance-profiling`.

### 🔬 3. Scientific Agent Toolkits (148 Skills)
- **Computational Physics & Math**: `astropy`, `fluidsim`, `sympy`, `pymoo`.
- **Structural Biology & Neuroscience**: `protein-structure-prediction`, `esm`, `molecular-dynamics`, `neurokit2`, `neuropixels-analysis`, `neuroscience-imaging`.
- **Machine Learning & Data Science**: `transformers`, `pytorch-lightning`, `scikit-learn`, `shap`, `umap-learn`, `polars`, `dask`, `networkx`, `seaborn`, `matplotlib`.
- **Scientific Communication & Grants**: `scientific-writing`, `literature-review`, `peer-review`, `research-grants`, `citation-management`, `latex-posters`, `markdown-mermaid-writing`.
- **Lab Automation**: `opentrons-integration`, `pylabrobot`, `lamindb`, `benchling-integration`, `protocolsio-integration`.


---

## 📁 Repository Structure

```
gemini-agent-toolkit/
├── gemini-skills/
│   ├── multimodal-video/      ← Video timelines and frame extraction
│   ├── search-grounding/      ← Live Google Search grounding
│   ├── structured-output/     ← Type-safe Pydantic JSON validation
│   ├── context-caching/       ← Cost-optimization cache managers
│   ├── function-calling/      ← External tool routing and triggers
│   ├── code-execution/        ← Native sandboxed Python runtime
│   └── audio-intelligence/    ← Native speech waveform understanding
├── examples/
│   ├── run_agent.py           ← Loads skills dynamically into System Instructions
│   ├── use_caching.py         ← Ready-to-run cache pipeline demonstration
│   └── use_grounding.py       ← Grounded search citation runner
├── scripts/
│   └── compile_skills.py      ← Compiler validator script for INDEX.json & combined MD
├── requirements.txt           ← SDK & validator library requirements
└── README.md                  ← This documentation file
```

---

## ⚙️ Quick Start Guide

### 1. Clone & Set Up Directory
```bash
git clone https://github.com/Lord1Egypt/gemini-agent-toolkit.git
cd gemini-agent-toolkit
```

### 2. Install Dependencies
Make sure you are using Python 3.11 (highly recommended for Vercel/serverless environments):
```bash
pip install -r requirements.txt
```

### 3. Compile & Validate Skills
Run the compiler script to validate frontmatter schemas and compile a single deployment system prompt:
```bash
python scripts/compile_skills.py
```
This generates:
- `INDEX.json`: Mapping index of descriptions, locations, and dependencies.
- `SYSTEM_INSTRUCTIONS.md`: A combined file containing all skills formatted for direct ingestion into Gemini's system instructions.

### 4. Run the Agent Example
Export your API key and execute the runner:
```bash
export GEMINI_API_KEY="your-google-api-key"
python examples/run_agent.py
```

---

## 📜 Contribution Guidelines

We encourage contributions! If you have optimized prompts or specific Gemini integration files:
1. Fork this repository.
2. Create a folder under `gemini-skills/your-skill-name/` containing `SKILL.md`.
3. Verify your YAML frontmatter includes `name`, `description`, `allowed-tools`, `license`, and `metadata.skill-author`.
4. Run `python scripts/compile_skills.py` to ensure validation passes.
5. Open a Pull Request.

---

<div align="center">

Made with ❤️ by **[Lord1Egypt](https://github.com/Lord1Egypt)**

[⭐ Star this repo](https://github.com/Lord1Egypt/gemini-agent-toolkit) · [🐛 Report an Issue](https://github.com/Lord1Egypt/gemini-agent-toolkit/issues) · [🔀 Submit a PR](https://github.com/Lord1Egypt/gemini-agent-toolkit/pulls)

</div>
