"""Entry script to launch the FastAPI preview app."""

from __future__ import annotations

import sys


def main() -> None:
    try:
        import uvicorn
    except ModuleNotFoundError:
        sys.stderr.write("FastAPI runtime dependencies are missing. Install project dependencies first.\n")
        sys.exit(1)

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
