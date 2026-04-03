# Writing Good System Prompts for Voice Agents

A guide based on best practices for building voice AI agents with real-time voice frameworks and native audio models like Gemini Live.

---

## Why System Prompts Matter More for Voice

Most voice agents fail at the system prompt level. A prompt written like a text document will produce an agent that sounds robotic, reads out bullet points, and drifts from its persona. Audio is a fundamentally different medium, the model is speaking, not writing an email.

---

## The 4 Techniques

### 1. Be Explicit About Persona and Scope

Don't just say "you are a helpful assistant." Tell the model:

- Who it is (give it a name)
- What it can and cannot do
- How to handle edge cases

**Bad:**

```text
You are a professional voice assistant. Your role is to help users search for contacts and dispatch outbound calls.
```

**Good:**

```text
You are Nova, a voice assistant for Luche Solutions. You help callers find contacts and dispatch outbound calls. You cannot help with anything outside of that — if someone asks about something unrelated, politely let them know and bring the conversation back on track.
```

---

### 2. Write for Audio, Not Text

Your agent is speaking, not writing a document. Apply these rules:

- Use short sentences
- Write in a natural, conversational tone
- Avoid bullet points, they don't translate to speech
- Avoid headers, the model may read them aloud or treat them as structure that disrupts flow
- Avoid markdown formatting entirely in the instructions body

**Bad:**

```text
# Call Flow
1. Greet the user professionally
2. Ask who they want to call
3. Use search_contact() to find the contact
```

**Good:**

```text
When a caller connects, greet them warmly and ask who they'd like to call. Search for the contact by name. If you find a match, read back the name and number clearly and ask if that's correct.
```

---

### 3. Add Guardrails Inline

Don't rely on a separate safety layer for basic redirection. If there are topics your agent should avoid or redirect, say so directly in the system prompt.

**Example:**

```text
You cannot help with anything outside of finding contacts and making calls. If someone asks about something unrelated, politely let them know you can only assist with those tasks, then bring the conversation back on track.
```

This keeps behavior predictable and reduces unexpected responses.

---

### 4. Shape the Voice with Director Notes

Native audio models like Gemini Live have deep audio understanding. You can instruct the model how to sound, and it will translate that directly into its delivery without extra config files or API calls.

You can specify:

- Tone: warm, confident, professional, casual
- Pace: slower, faster
- Energy: high energy, calm
- Accent: Irish, British, etc.

**Example:**

```text
Speak in a warm, confident, and professional tone. Keep your responses short — one or two sentences at most. Speak naturally, as if talking to someone directly, not writing to them.
```

---

## What NOT to Put in a Voice System Prompt

| Avoid | Why |
|---|---|
| Tool documentation (parameter lists, return values) | The model discovers tools via function signatures. This wastes tokens and reads like a README. |
| Bullet point lists of guidelines | They break conversational flow and may be read aloud |
| Section headers with `#` | Same issue, treat instructions as a spoken script, not a document |
| Vague persona ("be helpful and professional") | Too generic. Name the agent and define its exact scope. |

---

## Example: Before and After

### Before (document-style, text-first)

```yaml
instructions: |
  You are a professional voice assistant for Luche solutions company.
  Your role is to help users search for contacts and dispatch outbound calls.

  # Available Tools
  1. **search_contact(full_name)** - Search for a contact by name
  2. **collect_phone_number()** - Collect a 10-digit phone number via DTMF
  3. **add_to_call_list(phone_number)** - Add a number to the dispatch list
  4. **dispatch_call()** - Initiate calls to all numbers in the list

  # Tone & Guidelines
  - Be warm, professional, and concise
  - Keep responses to 1-2 sentences for voice clarity
```

### After (voice-first, audio-optimized)

```yaml
instructions: |
  You are Nova, a voice assistant for Luche Solutions. You help callers find
  contacts and dispatch outbound calls. Speak in a warm, confident, and
  professional tone. Keep your responses short — one or two sentences at most.
  Speak naturally, as if talking to someone directly, not writing to them.

  Your job is simple: help the caller build a list of contacts and then connect
  them. You cannot help with anything outside of that — if someone asks about
  something unrelated, politely let them know and bring the conversation back
  on track.

  When a caller connects, greet them warmly and ask who they'd like to call.
  Search for the contact by name. If you find a match, read back the name and
  number clearly and ask if that's correct. Once confirmed, add their number to
  the call list and ask if they'd like to add anyone else.

  Before dispatching, tell them how many contacts are in the list. Once they
  confirm, dispatch all the calls in sequence. Never proceed without explicit
  confirmation. Never read out a number without confirming it first.
```

---

## Additional Tips for Native Audio Models

- Multilingual support: native audio models can detect and switch languages automatically mid-conversation. To restrict languages, say so in the system prompt.
- Speaker drift: longer sessions can cause models to drift from the defined persona. Newer native audio models are designed to maintain persona and accent stability across long multi-turn conversations.
- Latency: native audio models process and generate audio directly instead of relying on a speech-to-text to speech pipeline, which results in lower latency and more natural delivery.
