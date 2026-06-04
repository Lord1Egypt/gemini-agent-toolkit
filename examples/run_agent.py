import os
import yaml
from google import genai

def load_skill_instruction(skill_name: str) -> str:
    """Loads a SKILL.md file and extracts the prompt instruction content.
    
    Bypasses the YAML frontmatter header and reads the markdown description.
    """
    skill_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "gemini-skills",
        skill_name,
        "SKILL.md"
    )
    if not os.path.exists(skill_path):
        raise FileNotFoundError(f"Skill '{skill_name}' not found at {skill_path}")
        
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split by frontmatter delimiters ---
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
            
    return content.strip()

def run_agent_with_skill(skill_name: str, query: str):
    # Initialize the client
    client = genai.Client()
    
    print(f"Loading skill: '{skill_name}'...")
    system_instruction = load_skill_instruction(skill_name)
    
    print(f"Initializing Gemini agent with specialized skill prompt...")
    # Inject loaded skill details as the System Instruction
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=query,
        config=dict(
            system_instruction=system_instruction
        )
    )
    
    print("\n--- Response ---")
    print(response.text)

if __name__ == "__main__":
    # Example using Structured Output instruction to analyze text
    text_query = (
        "We need to parse this: 'OpenAI announced GPT-5 yesterday at their headquarters in San Francisco. "
        "Sam Altman mentioned it would achieve full agentic capabilities.'"
    )
    # Check if Gemini API key is configured
    if "GEMINI_API_KEY" not in os.environ:
        print("⚠️ Warning: GEMINI_API_KEY env var not set. Run: export GEMINI_API_KEY='your-key'")
        
    run_agent_with_skill("structured-output", f"Extract details from this text: {text_query}")
