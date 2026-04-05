"""Export LiveKit telephony bridge payloads from local settings."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.integrations.telephony import export_bridge_config


def main() -> None:
    payload = export_bridge_config()
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
