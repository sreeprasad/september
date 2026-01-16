"""
Task 2: Test ElevenLabs Speech-to-Text
Run with: uv run python test_transcription.py <audio_file>
"""

import sys
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

def transcribe_audio(file_path: str) -> str:
    """Transcribe an audio file using ElevenLabs Speech-to-Text."""
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in .env file")
    
    client = ElevenLabs(api_key=api_key)
    
    print(f"📁 Transcribing: {file_path}")
    print("⏳ Processing...")
    
    with open(file_path, "rb") as audio_file:
        result = client.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1",  # ElevenLabs' transcription model
            language_code="en"
        )
    
    return result.text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python test_transcription.py <audio_file>")
        print("Example: uv run python test_transcription.py sample_call.mp3")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"❌ File not found: {audio_path}")
        sys.exit(1)
    
    try:
        transcript = transcribe_audio(audio_path)
        print("\n✅ Transcription successful!\n")
        print("=" * 50)
        print("TRANSCRIPT:")
        print("=" * 50)
        print(transcript)
        print("=" * 50)
        
        # Save transcript to file for use in Task 3
        output_file = "transcript_output.txt"
        with open(output_file, "w") as f:
            f.write(transcript)
        print(f"\n💾 Saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
