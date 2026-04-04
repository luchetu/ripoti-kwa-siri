"""Real-time voice runtime assembly for the prototype agent."""

from __future__ import annotations

from dataclasses import dataclass

from app.call_flow.controller import IntakeFlowController
from app.core.config import get_settings
from app.integrations.llm import load_voice_model_settings


@dataclass(frozen=True, slots=True)
class RealtimeSettings:
    url: str | None
    api_key: str | None
    api_secret: str | None
    agent_name: str = "sauti"


def realtime_dependencies_available() -> bool:
    """Return whether the real-time agent dependencies are importable."""

    try:
        import livekit  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def create_agent_server():
    """
    Create the real-time agent server using the current prompt and model config.

    The runtime imports are kept inside this function so local review of the repo
    does not require the voice stack to be installed immediately.
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
    intake = IntakeFlowController.from_prompt_path(settings.prompt_path)

    class SautiAgent(Agent):
        def __init__(self) -> None:
            super().__init__(instructions=intake.instructions)

    server = AgentServer()

    def prewarm(proc: JobProcess) -> None:
        proc.userdata["vad"] = None  # Gemini Live handles turn-taking; VAD not required

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
            room_input_options=room_io.RoomInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVC(),
            ),
        )
        await ctx.connect()

    return server


def run() -> None:
    """Run the real-time agent server via the framework CLI."""

    from livekit.agents import cli

    cli.run_app(create_agent_server())
