"""Create inbound SIP telephony resources for ripoti-kwa-siri."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.integrations.telephony import (
    build_livekit_dispatch_rule_request,
    build_livekit_inbound_trunk_request,
    export_bridge_config,
)


async def _find_existing_resources(
    lkapi,
    *,
    trunk_name: str,
    rule_name: str,
) -> tuple[object | None, object | None]:
    from livekit import api

    trunk_response = await lkapi.sip.list_inbound_trunk(api.ListSIPInboundTrunkRequest())
    existing_trunk = next((item for item in trunk_response.items if item.name == trunk_name), None)

    rule_response = await lkapi.sip.list_dispatch_rule(api.ListSIPDispatchRuleRequest())
    existing_rule = next((item for item in rule_response.items if item.name == rule_name), None)

    return existing_trunk, existing_rule


async def _apply() -> None:
    from livekit import api

    bridge_config = export_bridge_config()
    inbound_name = bridge_config["inbound_trunk"]["name"]
    dispatch_name = bridge_config["dispatch_rule"]["name"]

    print("Planned telephony bridge configuration:")
    print(json.dumps(bridge_config, indent=2))
    print()

    async with api.LiveKitAPI() as lkapi:
        existing_trunk, existing_rule = await _find_existing_resources(
            lkapi,
            trunk_name=str(inbound_name),
            rule_name=str(dispatch_name),
        )

        if existing_trunk is None:
            created_trunk = await lkapi.sip.create_inbound_trunk(
                build_livekit_inbound_trunk_request()
            )
            print(f"Created inbound trunk: {created_trunk.sip_trunk_id} ({created_trunk.name})")
        else:
            print(f"Inbound trunk already exists: {existing_trunk.sip_trunk_id} ({existing_trunk.name})")

        if existing_rule is None:
            created_rule = await lkapi.sip.create_dispatch_rule(
                build_livekit_dispatch_rule_request()
            )
            print(
                f"Created dispatch rule: {created_rule.sip_dispatch_rule_id} ({created_rule.name})"
            )
        else:
            print(
                f"Dispatch rule already exists: {existing_rule.sip_dispatch_rule_id} ({existing_rule.name})"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the LiveKit inbound trunk and dispatch rule for ripoti-kwa-siri."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create missing resources in LiveKit. Without this flag, only print the planned configuration.",
    )
    args = parser.parse_args()

    if not args.apply:
        print(json.dumps(export_bridge_config(), indent=2))
        print()
        print("Dry run only. Re-run with --apply to create missing LiveKit resources.")
        return

    asyncio.run(_apply())


if __name__ == "__main__":
    main()
