---
name: audio-intelligence
description: Native audio understanding, transcription, speech tone analysis, sound classification, and multi-speaker transcription.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Multimodal Audio Intelligence Skill

## Overview
This skill describes how to utilize Gemini's native audio understanding. Unlike standard pipeline models that transcribe audio via a separate automatic speech recognition (ASR) system before processing, Gemini consumes audio waveforms directly. This allows it to capture acoustic details like tone, speed, emotion, speaker transitions, and environmental sounds.

---

## When to Use This Skill
- Transcribing speeches, interviews, podcasts, or call logs.
- Performing audio-based sentiment analysis (detecting anger, sarcasm, or nervousness).
- Sound classification (detecting police sirens, glass breaking, background rain).
- Dynamic Q&A over long-form lectures or recorded meetings.

---

## Quick Start (with runnable code examples)

```python
import time
from google import genai

# Initialize the Gemini GenAI Client
client = genai.Client()

def analyze_audio(audio_path: str):
    print("Uploading audio file to Gemini...")
    audio_file = client.files.upload(file=audio_path)
    
    # Wait for file processing to complete
    while audio_file.state.name == "PROCESSING":
        print("Waiting for audio processing to finish...")
        time.sleep(3)
        audio_file = client.files.get(name=audio_file.name)
        
    if audio_file.state.name != "ACTIVE":
        raise ValueError(f"Audio upload failed with state: {audio_file.state.name}")
        
    print(f"Audio ready! URL: {audio_file.uri}")
    
    # Query Gemini to transcribe and analyze the audio
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            audio_file,
            (
                "Perform three tasks on this audio file:\n"
                "1. Provide a verbatim transcription.\n"
                "2. Analyze the speaker's emotional state, tone, and pacing.\n"
                "3. List any significant background noises or sound effects."
            )
        ]
    )
    
    print("\n--- Audio Transcription & Analysis ---")
    print(response.text)
    
    # Cleanup
    print("\nCleaning up audio resource...")
    client.files.delete(name=audio_file.name)

if __name__ == "__main__":
    # Example audio path
    analyze_audio("sample_audio.wav")
```

---

## Advanced Usage

### Audio Question-Answering (Temporal Spotting)
You can query the audio timeline to locate specific speech cues or extract timestamps:

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        audio_file,
        "What is the speaker discussing at the 02:45 mark? Answer in detail."
    ]
)
```

---

## Key References
- [Google GenAI File API Audio Guide](https://github.com/googleapis/python-genai)
- Gemini Audio Capabilities Reference

---

## Dependencies
- `google-genai>=0.1.1`
- `pydub` (optional, for local audio conversion/segmentation)
