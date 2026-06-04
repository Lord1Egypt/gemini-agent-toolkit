import os
import json
from google import genai

INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "INDEX.json")
SKILLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gemini-skills")

def load_skills_index():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"Index file not found at {INDEX_PATH}. Please run compile_skills.py first.")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_skill_body(skill_folder_name: str) -> str:
    skill_path = os.path.join(SKILLS_DIR, skill_folder_name, "SKILL.md")
    if not os.path.exists(skill_path):
        return ""
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Strip YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()

def route_query_to_skills(client: genai.Client, query: str, skills_list: list) -> list[str]:
    """Uses a light, fast call to Gemini to match the query to the best 1-2 skills."""
    print("🤖 Router: Selecting best skills from the 198 options...")
    
    # Prepare a compact representation of the index
    compact_index = [
        {"name": s["name"], "description": s["description"]}
        for s in skills_list
    ]
    
    router_prompt = (
        "You are an API router. You will be given a list of skills and a user query.\n"
        "Your task is to select the 1 or 2 most relevant skills that are absolutely necessary to answer the query.\n\n"
        f"Available Skills:\n{json.dumps(compact_index, indent=1)}\n\n"
        f"User Query: '{query}'\n\n"
        "Instructions:\n"
        "1. Identify the matching skills.\n"
        "2. Output ONLY the skill names as a comma-separated list (e.g. 'search-grounding, database-lookup').\n"
        "3. If no skills are relevant, output 'none'.\n"
        "4. Do NOT output any reasoning, introductory, or formatting text."
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=router_prompt
    )
    
    selection = response.text.strip().lower()
    if not selection or selection == "none":
        return []
        
    # Split and clean skill names
    selected_skills = [s.strip() for s in selection.split(",") if s.strip()]
    return selected_skills

def chat_session_loop():
    print("Initializing Gemini Client...")
    client = genai.Client()
    
    # Load index
    skills_index = load_skills_index()
    print(f"Loaded index of {len(skills_index)} agent skills.")
    
    while True:
        try:
            print("\n" + "="*50)
            user_query = input("Ask Gemini (or type 'exit' to quit): ").strip()
            if not user_query:
                continue
            if user_query.lower() in ["exit", "quit"]:
                print("Exiting chat session.")
                break
                
            # 1. Routing step (Dynamic Selection)
            selected_names = route_query_to_skills(client, user_query, skills_index)
            
            # 2. Load instructions
            sys_instructions = [
                "You are an advanced agent. Use the loaded skills to answer the user query."
            ]
            if selected_names:
                print(f"🎯 Dynamic Match: Loading skills: {', '.join(selected_names)}")
                for name in selected_names:
                    # Find directory name (matches name)
                    body = load_skill_body(name)
                    if body:
                        sys_instructions.append(f"=== SKILL: {name} ===\n{body}")
            else:
                print("ℹ️ Router: No matching domain skills needed. Running generic model context.")
                
            combined_system_prompt = "\n\n".join(sys_instructions)
            
            # 3. Stream final query response
            print("\n💬 Agent Response:")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_query,
                config=dict(
                    system_instruction=combined_system_prompt
                )
            )
            print(response.text)
            
        except KeyboardInterrupt:
            print("\nExiting chat session.")
            break
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        print("⚠️ Warning: GEMINI_API_KEY environment variable is not set.")
        print("Please run: export GEMINI_API_KEY='your-api-key'")
        
    chat_session_loop()
