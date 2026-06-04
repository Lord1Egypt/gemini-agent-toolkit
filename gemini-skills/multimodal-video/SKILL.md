---
name: multimodal-video
description: Native video understanding, event timestamping, frame sampling, and video narrative generation.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Multimodal Video Intelligence Skill

## Overview
This skill outlines how to leverage Google's Gemini models (such as `gemini-2.5-flash` or `gemini-2.5-pro`) to process video files natively without pre-extracting audio or individual image frames manually.

Gemini accepts direct video file inputs (up to 50MB directly in generation, or up to 2GB via the File API) and performs multimodal fusion over audio tracks, spatial layouts, and temporal transitions.

---

## When to Use This Skill
- For temporal query-answering (e.g., "At what timestamp does the red car appear?").
- Summarizing lecture, security camera, or gaming videos.
- Extracting specific textual details or visual overlays from video sequences.
- Translating or transcribing speech combined with on-screen visual context.

---

## Quick Start (with runnable code examples)

```python
import time
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

def analyze_video(video_path: str):
    print("Uploading video file to Gemini File API...")
    video_file = client.files.upload(file=video_path)
    
    # Poll for file state until it transitions from PROCESSING to ACTIVE
    while video_file.state.name == "PROCESSING":
        print("Waiting for video to be processed by Google servers...")
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)
        
    if video_file.state.name != "ACTIVE":
        raise ValueError(f"File upload failed with state: {video_file.state.name}")
        
    print(f"Video file is ready! URI: {video_file.uri}")
    
    # Query the video using gemini-2.5-flash
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            video_file,
            "Provide a bulleted timeline of events in this video. Format each event as [MM:SS] - Description."
        ]
    )
    
    print("\n--- Video Timeline Analysis ---")
    print(response.text)
    
    # Cleanup: Delete file from Gemini storage after processing
    print("\nCleaning up remote video file...")
    client.files.delete(name=video_file.name)

if __name__ == "__main__":
    # Example video path
    analyze_video("sample_video.mp4")
```

---

## Advanced Usage

### Temporal Search (Visual Event Identification)
To locate highly specific occurrences inside a long clip, specify the frame rate or use clear timeline descriptions in the prompt:

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        video_file,
        "Examine the video closely. Find the exact start and end timestamps where a person is wearing a blue shirt. Output ONLY the timestamps in JSON format: {'start': 'MM:SS', 'end': 'MM:SS'}."
    ],
    config=dict(
        response_mime_type="application/json"
    )
)
```

---

## Key References
- [Google GenAI File API Documentation](https://github.com/googleapis/python-genai)
- Gemini Multimodal Capabilities Guide

---

## Dependencies
- `google-genai>=0.1.1`
- `ffmpeg` (optional, for local video clipping/resizing before upload)
