# Real-Time Voice Runtime

This note captures the minimal runtime wiring for the prototype voice agent.

## Components

- `run_agent.py`: entry script to launch the real-time server
- `app/integrations/realtime.py`: builds the agent server and session
- `app/integrations/llm.py`: model settings (STT/LLM/TTS)
- `prompts/anonymous_reporting_agent.yaml`: runtime prompt
- `.env.local`: environment for realtime URL/key/secret and model choices

## Environment

Required:
- `REALTIME_URL`
- `REALTIME_API_KEY`
- `REALTIME_API_SECRET`
- `GOOGLE_API_KEY` (Gemini Live)

Defaults you can override:
- `VOICE_AGENT_NAME` (default `sauti`)
- `VOICE_LIVE_MODEL` (default `google/gemini-2.5-flash-native-audio-preview-12-2025`)
- `VOICE_LIVE_VOICE` (default `Puck`)
- `VOICE_PREEMPTIVE_GENERATION` (default `true`)

Optional (for future telephony):
- `TELEPHONY_ACCOUNT_SID`
- `TELEPHONY_AUTH_TOKEN`
- `TELEPHONY_NUMBER`

## Running (uv)

```bash
uv sync
cp .env.example .env.local  # then fill in keys
uv run run_agent.py
```

If the voice dependencies are missing, `run_agent.py` will exit with a clear message.
