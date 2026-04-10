"""Entry script to launch the real-time voice agent server."""

from __future__ import annotations

import sys

from src.infrastructure.voice.agent import realtime_dependencies_available, run


def main() -> None:
    if not realtime_dependencies_available():
        sys.stderr.write(
            "Real-time agent dependencies are missing. "
            "Install the voice runtime extras before running.\n"
        )
        sys.exit(1)
    run()


if __name__ == "__main__":
    main()
