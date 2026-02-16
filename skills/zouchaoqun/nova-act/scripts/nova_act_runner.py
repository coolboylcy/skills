#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "nova-act",
#     "pydantic>=2.0",
#     "fire",
# ]
# ///
"""
Run browser automation tasks using Amazon Nova Act.

Usage:
    uv run nova_act_runner.py --url "https://google.com/flights" --task "Find flights from SFO to NYC and return the options"
"""

import json
import os
import sys
from urllib.parse import urlparse

from pydantic import BaseModel


class TaskResult(BaseModel):
    """Generic result schema for any browser task."""
    summary: str
    details: list[str]


ALLOWED_SCHEMES = {"http", "https"}

MATERIAL_IMPACT_KEYWORDS = [
    "buy", "purchase", "checkout", "pay", "subscribe", "donate", "order",
    "post", "publish", "share", "send", "email", "message", "tweet",
    "sign up", "register", "create account", "join",
    "submit", "apply", "enroll", "book", "reserve",
    "delete", "remove", "cancel",
]


def validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        print(f"Error: URL scheme must be http or https, got: {parsed.scheme!r}", file=sys.stderr)
        sys.exit(1)
    if not parsed.netloc:
        print(f"Error: URL must include a hostname: {url}", file=sys.stderr)
        sys.exit(1)
    return url


def validate_task(task: str) -> str:
    if not task or not task.strip():
        print("Error: Task description cannot be empty", file=sys.stderr)
        sys.exit(1)
    if len(task) > 2000:
        print(f"Error: Task too long ({len(task)} chars, max 2000)", file=sys.stderr)
        sys.exit(1)
    return task.strip()


def check_material_impact(task: str) -> None:
    task_lower = task.lower()
    triggered = [kw for kw in MATERIAL_IMPACT_KEYWORDS if kw in task_lower]
    if triggered:
        print(f"Warning: Task may involve material-impact actions ({', '.join(triggered)}). "
              f"Will stop before completing irreversible actions.", file=sys.stderr)


def run(url: str, task: str) -> None:
    """
    Run a browser automation task with Nova Act.

    Args:
        url: Starting URL to navigate to
        task: Task to perform and return results (e.g., "Find flights from SFO to NYC and return the options")
    """
    url = validate_url(url)
    task = validate_task(task)
    check_material_impact(task)

    api_key = os.environ.get("NOVA_ACT_API_KEY")
    if not api_key:
        print("Error: NOVA_ACT_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    from nova_act import NovaAct

    try:
        with NovaAct(starting_page=url) as nova:
            # act_get performs the task AND extracts results in one call
            result = nova.act_get(task, schema=TaskResult.model_json_schema())

            # Parse and output
            task_result = TaskResult.model_validate(result.parsed_response)
            print(json.dumps(task_result.model_dump(), indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    import fire
    fire.Fire(run)


if __name__ == "__main__":
    main()
