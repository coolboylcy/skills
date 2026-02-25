# OpenAI

## Base URL
```
https://api.openai.com/v1
```

## Authentication
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /chat/completions | POST | Chat/GPT models |
| /embeddings | POST | Text embeddings |
| /images/generations | POST | DALL-E images |
| /audio/transcriptions | POST | Whisper STT |
| /audio/speech | POST | TTS |
| /models | GET | List models |

## Quick Examples

### Chat Completion
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Streaming Chat
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

### Create Embedding
```bash
curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-3-small",
    "input": "Your text here"
  }'
```

### Generate Image
```bash
curl https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A white cat",
    "size": "1024x1024"
  }'
```

### Transcribe Audio
```bash
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 \
  -F model=whisper-1
```

## Models

| Model | Use Case |
|-------|----------|
| gpt-4o | Best overall |
| gpt-4o-mini | Fast, cheap |
| gpt-4-turbo | Previous best |
| text-embedding-3-small | Embeddings (cheap) |
| text-embedding-3-large | Embeddings (better) |
| dall-e-3 | Image generation |
| whisper-1 | Speech to text |
| tts-1 | Text to speech |

## Common Traps

- Max tokens includes input + output
- Streaming responses are SSE format
- Image URLs expire after 1 hour
- Whisper max file size: 25MB
- Rate limits vary by model and tier

## Rate Limits

Varies by tier and model. Check:
```bash
# Response headers include:
x-ratelimit-limit-requests
x-ratelimit-remaining-requests
x-ratelimit-reset-requests
```

## Official Docs
https://platform.openai.com/docs/api-reference
