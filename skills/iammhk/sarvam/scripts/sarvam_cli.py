import os
import sys
import argparse
import requests
import json
import base64

# Set your API key here or in environment variable
API_KEY = os.environ.get("SARVAM_API_KEY")

if not API_KEY:
    print("Error: SARVAM_API_KEY environment variable not set.")
    sys.exit(1)

BASE_URL = "https://api.sarvam.ai"

def text_to_speech(text, target_language_code, speaker, output_file, model="bulbul:v3"):
    url = f"{BASE_URL}/text-to-speech"
    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": [text],
        "target_language_code": target_language_code,
        "speaker": speaker,
        "pace": 1.0,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": model
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        audio_data = response.json()
        # The API returns base64 encoded audio in "audios" list
        if "audios" in audio_data and len(audio_data["audios"]) > 0:
            audio_bytes = base64.b64decode(audio_data["audios"][0])
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            print(f"Audio saved to {output_file}")
            print(f"MEDIA:{os.path.abspath(output_file)}")
        else:
             print("Error: No audio data received.")
             print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error during TTS request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

def speech_to_text(audio_file, model="saaras:v3", mode="transcribe"): # Updated default model
    url = f"{BASE_URL}/speech-to-text"
    headers = {
        "api-subscription-key": API_KEY,
    }
    
    # MIME type detection (basic)
    if audio_file.endswith(".wav"):
        mime_type = "audio/wav"
    elif audio_file.endswith(".mp3"):
        mime_type = "audio/mpeg"
    else:
        mime_type = "audio/wav" # Default
        
    try:
        with open(audio_file, "rb") as f:
            files = {
                "file": (os.path.basename(audio_file), f, mime_type)
            }
            data = {
                "model": model,
                "mode": mode
                 # "prompt": "" # Optional prompt
            }
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            print(json.dumps(response.json(), indent=2))
            
    except requests.exceptions.RequestException as e:
        print(f"Error during STT request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)
    except FileNotFoundError:
        print(f"Error: Audio file not found: {audio_file}")


def translate(text, source_lang, target_lang, speaker_gender="Male"):
    url = f"{BASE_URL}/translate"
    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "source_language_code": source_lang,
        "target_language_code": target_lang,
        "speaker_gender": speaker_gender,
        "mode": "formal", # formal/informal
        "model": "mayuri:v1"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error during Translation request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

def chat_completion(message, model="sarvam-2g", system_prompt=None):
    url = f"{BASE_URL}/chat/completions" # Note: docs say /chat/completions for OpenAI compat, or maybe /v1/chat/completions?
    # Quickstart curl says: https://api.sarvam.ai/v1/chat/completions but python/js SDK uses client.chat.completions
    # Let's try https://api.sarvam.ai/chat/completions based on other endpoints, or stick to v1 if documented.
    # The curl example in docs explicitly used: https://api.sarvam.ai/v1/chat/completions
    
    url = "https://api.sarvam.ai/chat/completions" # Based on pattern, but let's check docs again. Docs curl: https://api.sarvam.ai/v1/chat/completions
    # Wait, the quickstart text I read said: "curl -X POST https://api.sarvam.ai/v1/chat/completions"
    url = "https://api.sarvam.ai/v1/chat/completions"

    headers = {
        "api-subscription-key": API_KEY, # Or Authorization: Bearer? Docs curl used Authorization: Bearer $SARVAM_API_KEY
        "Content-Type": "application/json"
        # "Authorization": f"Bearer {API_KEY}" # Let's try this if api-subscription-key fails, or both.
        # Docs say: -H "Authorization: Bearer $SARVAM_API_KEY"
    }
    # However, other endpoints used api-subscription-key header. 
    # Let's try adding both or stick to what docs said for chat specifically.
    
    # Actually, the quickstart curl for chat used: -H "Authorization: Bearer $SARVAM_API_KEY"
    # But for others it used: -H "api-subscription-key: <YOUR_SARVAM_API_KEY>"
    # I will support the header based on the specific endpoint documentation.
    
    # Chat headers
    chat_headers = {
         "Authorization": f"Bearer {API_KEY}",
         "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": message})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload, headers=chat_headers)
        response.raise_for_status()
        result = response.json()
        
        # Print just the content for easy reading, or full json? 
        # Let's print full json for machine readability, but also the text.
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            print(content)
        else:
            print(json.dumps(result, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error during Chat request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

def main():
    parser = argparse.ArgumentParser(description="Sarvam AI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # TTS Command
    tts_parser = subparsers.add_parser("tts", help="Text to Speech")
    tts_parser.add_argument("text", help="Text to convert to speech")
    tts_parser.add_argument("--lang", default="hi-IN", help="Target language code (e.g., hi-IN, bn-IN)")
    tts_parser.add_argument("--speaker", default="priya", help="Speaker voice (e.g., priya, amit, etc.)")
    tts_parser.add_argument("--model", default="bulbul:v3", help="Model (bulbul:v3)")
    tts_parser.add_argument("--output", "-o", default="output.wav", help="Output audio file path")

    # STT Command
    stt_parser = subparsers.add_parser("stt", help="Speech to Text")
    stt_parser.add_argument("file", help="Path to audio file")
    stt_parser.add_argument("--model", default="saaras:v3", help="Model to use (saaras:v3)") # Updated default
    stt_parser.add_argument("--mode", default="transcribe", choices=["transcribe", "translate", "verbatim", "translit", "codemix"], help="STT Mode") # Added mode

    # Translate Command
    trans_parser = subparsers.add_parser("translate", help="Translate text")
    trans_parser.add_argument("text", help="Text to translate")
    trans_parser.add_argument("--source", default="en-IN", help="Source language code")
    trans_parser.add_argument("--target", default="hi-IN", help="Target language code")

    # Chat Command
    chat_parser = subparsers.add_parser("chat", help="Chat Completion")
    chat_parser.add_argument("message", help="User message")
    chat_parser.add_argument("--model", default="sarvam-2g", help="Model (sarvam-2g)")
    chat_parser.add_argument("--system", help="System prompt (optional)")

    args = parser.parse_args()

    if args.command == "tts":
        text_to_speech(args.text, args.lang, args.speaker, args.output, args.model)
    elif args.command == "stt":
        speech_to_text(args.file, args.model, args.mode)
    elif args.command == "translate":
        translate(args.text, args.source, args.target)
    elif args.command == "chat":
        chat_completion(args.message, args.model, args.system)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
