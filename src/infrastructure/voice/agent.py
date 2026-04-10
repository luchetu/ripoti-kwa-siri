"""SautiAgent — the real-time voice agent backed by Gemini Live."""

from __future__ import annotations

from dataclasses import dataclass

from src.infrastructure.config.settings import extract_yaml_block, get_settings
from src.infrastructure.voice.model_settings import load_voice_model_settings


@dataclass(frozen=True, slots=True)
class RealtimeSettings:
    url: str | None
    api_key: str | None
    api_secret: str | None
    agent_name: str = "sauti"


def realtime_dependencies_available() -> bool:
    try:
        import livekit  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def create_agent_server():
    """
    Build the LiveKit AgentServer with SautiAgent.

    Imports are deferred so the repo can be reviewed without installing
    the full voice stack.
    """
    from livekit.agents import Agent, AgentServer, AgentSession, JobContext, JobProcess, room_io
    from livekit.plugins import google, noise_cancellation

    settings = get_settings()
    model_settings = load_voice_model_settings()
    realtime_settings = RealtimeSettings(
        url=settings.realtime_url,
        api_key=settings.realtime_api_key,
        api_secret=settings.realtime_api_secret,
        agent_name=settings.voice_agent_name,
    )
    instructions = extract_yaml_block(settings.prompt_path, "instructions")

    class SautiAgent(Agent):
        def __init__(self) -> None:
            super().__init__(instructions=instructions)

    server = AgentServer()

    def prewarm(proc: JobProcess) -> None:
        proc.userdata["vad"] = None  # Gemini Live handles turn-taking

    server.setup_fnc = prewarm

    @server.rtc_session(agent_name=realtime_settings.agent_name)
    async def session_entrypoint(ctx: JobContext) -> None:
        ctx.log_context_fields = {"room": ctx.room.name}
        session = AgentSession(
            llm=google.realtime.RealtimeModel(
                model=model_settings.live_model,
                voice=model_settings.live_voice,
            ),
            preemptive_generation=model_settings.preemptive_generation,
        )
        await session.start(
            agent=SautiAgent(),
            room=ctx.room,
            room_options=room_io.RoomOptions(
                audio_input=room_io.AudioInputOptions(
                    noise_cancellation=lambda params: noise_cancellation.BVC(),
                ),
            ),
        )
        await ctx.connect()
        await session.generate_reply(
            instructions="Greet the caller, introduce yourself as Sauti, and invite them to explain what happened."
        )

    return server


def run() -> None:
    from livekit.agents import cli
    cli.run_app(create_agent_server())
