import os
from google import genai

def run_grounded_search():
    client = genai.Client()
    
    query = "Who is leading the current Formula 1 World Championship standings right now?"
    print(f"Executing Google Search Grounded query: '{query}'")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=query,
        config=dict(
            # Enable live Google Search grounding
            tools=[{'google_search': {}}]
        )
    )
    
    print("\n=== Answer ===")
    print(response.text)
    
    # Extract metadata chunks
    metadata = response.candidates[0].grounding_metadata
    if metadata and metadata.grounding_chunks:
        print("\n=== Sources & Citations ===")
        for idx, chunk in enumerate(metadata.grounding_chunks, 1):
            web = chunk.web
            if web:
                print(f"[{idx}] {web.title}")
                print(f"    Link: {web.uri}")
                
        # Search Entry Point HTML snippet
        if metadata.search_entry_point:
            print("\n=== Search Entry HTML ===")
            print(metadata.search_entry_point.rendered_content_html)
    else:
        print("\nNo grounding metadata was returned.")

if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        print("⚠️ Warning: GEMINI_API_KEY env var not set. Run: export GEMINI_API_KEY='your-key'")
    run_grounded_search()
