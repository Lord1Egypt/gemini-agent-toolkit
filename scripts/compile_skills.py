import os
import json
from pathlib import Path

SKILLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gemini-skills")
OUTPUT_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "INDEX.json")
OUTPUT_MD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SYSTEM_INSTRUCTIONS.md")

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse basic YAML-like frontmatter without external library dependencies."""
    if not content.startswith("---"):
        return {}, content
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
        
    yaml_text = parts[1].strip()
    body = parts[2].strip()
    
    metadata = {}
    current_key = None
    
    for line in yaml_text.splitlines():
        # Track original indentation to detect nested fields
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            
            # Remove surrounding quotes if present
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
                
            # Check if this line is indented (a child of the parent metadata key)
            if line.startswith(" ") or line.startswith("\t"):
                if current_key and isinstance(metadata.get(current_key), dict):
                    metadata[current_key][key] = val
                else:
                    metadata[key] = val
            else:
                if key == "metadata":
                    metadata[key] = {}
                    current_key = "metadata"
                else:
                    metadata[key] = val
                    current_key = key
                    
    return metadata, body


def compile_all_skills():
    print(f"Scanning skills directory: {SKILLS_DIR}...")
    base_path = Path(SKILLS_DIR)
    
    if not base_path.exists():
        print(f"Error: Directory {SKILLS_DIR} does not exist.")
        return
        
    skill_folders = sorted([d for d in base_path.iterdir() if d.is_dir()])
    compiled_skills = []
    
    # Combined Markdown build
    md_content = [
        "# Gemini Agent Toolkit — Unified System Instructions",
        "This file aggregates all loaded agent instructions. Import this into Gemini's system instructions to give it multi-skill agent workflows.",
        ""
    ]
    
    # Only name and description are strictly required for index/instructions
    required_fields = ["name", "description"]
    
    for folder in skill_folders:
        skill_file = folder / "SKILL.md"
        if not skill_file.exists():
            print(f"  ⚠️ Skipping {folder.name} (SKILL.md does not exist)")
            continue
            
        print(f"  Processing {folder.name}...")
        with open(skill_file, "r", encoding="utf-8") as f:
            raw_content = f.read()
            
        metadata, body = parse_frontmatter(raw_content)
        
        # Validation checks
        missing = [f for f in required_fields if f not in metadata]
        if missing:
            print(f"  ❌ Validation Error in {folder.name}: Missing fields: {missing}")
            continue
            
        # Get optional fields with fallbacks
        allowed_tools = metadata.get("allowed-tools", "Read Write Edit Bash")
        license_str = metadata.get("license", "BSD-3-Clause license")
        meta_dict = metadata.get("metadata", {})
        if not isinstance(meta_dict, dict):
            meta_dict = {}
        author = meta_dict.get("skill-author", "Lord1Egypt")
        
        compiled_skills.append({
            "name": metadata["name"],
            "description": metadata["description"],
            "allowed_tools": allowed_tools,
            "license": license_str,
            "author": author,
            "path": f"gemini-skills/{folder.name}/SKILL.md"
        })
        
        # Append to combined instruction markdown
        md_content.append(f"## Skill: {metadata['name']}")
        md_content.append(f"**Description**: {metadata['description']}")
        md_content.append(f"**Allowed Tools**: {allowed_tools}")
        md_content.append("")
        md_content.append(body)
        md_content.append("\n---\n")


        
    # Write JSON index
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(compiled_skills, f, indent=2)
    print(f"\n✅ Index JSON successfully compiled to: {OUTPUT_JSON}")
    
    # Write Markdown aggregator
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    print(f"✅ Combined markdown instructions compiled to: {OUTPUT_MD}")
    
    print(f"Processed {len(compiled_skills)} skills successfully.")

if __name__ == "__main__":
    compile_all_skills()
