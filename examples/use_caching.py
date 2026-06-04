import os
import time
from google import genai

def run_caching_pipeline():
    client = genai.Client()
    
    # 1. Create a dummy large document content block
    document_content = (
        "Project Orion System Architecture Specification.\n"
        "Created: 2026-06-04 by Team Alpha.\n\n"
        "Section 1: Microservice Router\n"
        "The router handles all incoming HTTP payloads and maps requests to serverless instances.\n"
        "It applies custom rate limits at 100 requests per minute per IP.\n\n"
        "Section 2: Database Storage\n"
        "We utilize Upstash Redis for distributed cache storage and session management.\n"
        "PostgreSQL serves as the main transactional database database, configured with SSL on port 5432.\n\n"
        "Section 3: Security Controls\n"
        "All API keys must be encrypted at rest using AES-256-GCM. No secrets can be saved in code repositories."
    )
    
    print("Writing temporary document structure...")
    temp_path = "orion_architecture.txt"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(document_content)
        
    try:
        # 2. Upload file
        print("Uploading file to Gemini File API...")
        uploaded_file = client.files.upload(file=temp_path)
        
        while uploaded_file.state.name == "PROCESSING":
            print("Processing file...")
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)
            
        print(f"File uploaded successfully: {uploaded_file.name}")
        
        # 3. Create context cache
        print("\nCreating Context Cache...")
        cache = client.caches.create(
            model='gemini-2.5-flash',
            config=dict(
                contents=[uploaded_file],
                ttl='600s', # 10 minute expiration
                display_name="orion_arch_specification_cache"
            )
        )
        print(f"Cache registered: {cache.name}")
        
        # 4. Perform multiple cached queries
        queries = [
            "Which database is used for main transactional workloads according to Section 2?",
            "What is the rate limit configuration in Section 1?",
            "What encryption algorithm is recommended for API keys in Section 3?"
        ]
        
        for idx, query in enumerate(queries, 1):
            print(f"\n--- Run Query {idx}: '{query}' ---")
            t0 = time.time()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=query,
                config=dict(
                    cached_content=cache.name
                )
            )
            elapsed = time.time() - t0
            print(f"Answer: {response.text.strip()}")
            print(f"Duration: {elapsed:.2f} seconds")
            
        # 5. Clean up
        print("\nCleaning up cache and files...")
        client.caches.delete(name=cache.name)
        client.files.delete(name=uploaded_file.name)
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("Temporary local file deleted.")

if __name__ == "__main__":
    if "GEMINI_API_KEY" not in os.environ:
        print("⚠️ Warning: GEMINI_API_KEY env var not set. Run: export GEMINI_API_KEY='your-key'")
    run_caching_pipeline()
