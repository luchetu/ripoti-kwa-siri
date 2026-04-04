# Prompts

This folder holds voice-agent prompts for `ripoti-kwa-siri`.

The goal is to keep prompts separate from code so we can iterate on behavior, tone, guardrails, and conversation flow before implementation details settle.

## Files

- `anonymous_reporting_agent.yaml`: the main runtime system prompt for the caller-facing voice agent

## Format Convention

- always store prompts as `.yaml`
- keep prompt content in a top-level `instructions` field unless a file needs more structure
- use YAML so prompts are easy to load, version, and extend with metadata later

## Prompt Design Notes

- write for speech, not for documents
- use short natural sentences
- keep the agent narrow in scope
- include privacy guardrails directly in the prompt
- avoid promising technical guarantees the system has not yet implemented
