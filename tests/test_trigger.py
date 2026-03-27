"""Layer 2: Trigger quality evals.

Tests that each skill is invoked (or not) by Claude for the queries defined
in skills/*/evals/trigger-evals.json. Requires the claude CLI and
ANTHROPIC_API_KEY to be set.
"""

from __future__ import annotations

import json
import os
import select
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not shutil.which("claude"),
    reason="claude CLI not installed",
)

_TEMPLATE_DIR = Path(__file__).parent / ".claude-template"


def _run_trigger_query(
    query: str,
    skill_path: Path,
    skill_name: str,
    artifacts_dir: Path | None = None,
    timeout: int = 30,
    model: str | None = None,
) -> bool:
    """Return True if Claude invokes the skill for the given query.

    Creates an isolated Claude config directory from the template, copies the
    whole skill directory into its skills/ folder, then runs the query via
    `claude -p` with CLAUDE_CONFIG_DIR pointing at that temp directory so
    ~/.claude/ is never consulted.

    If artifacts_dir is given, the raw stream-json output is written to
    raw.ndjson for post-mortem inspection. Use `jq` to explore it:
      jq 'select(.type == "result")' raw.ndjson
      jq '... | select(.event.type == "content_block_delta" and
            .event.delta.type == "thinking_delta") | .event.delta.thinking' raw.ndjson
    """
    tmp_config = Path(tempfile.mkdtemp(prefix="claude-eval-"))

    try:
        shutil.copytree(_TEMPLATE_DIR, tmp_config, dirs_exist_ok=True)
        shutil.copytree(skill_path, tmp_config / "skills" / skill_name)

        cmd = [
            "claude", "-p", query,
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
        if model:
            cmd += ["--model", model]

        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        env["CLAUDE_CONFIG_DIR"] = str(tmp_config)

        artifact = open(artifacts_dir / "raw.ndjson", "wb") if artifacts_dir else None
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=str(Path(__file__).parent.parent),
            env=env,
        )

        triggered = False
        start = time.time()
        buf = ""
        pending_tool: str | None = None
        accumulated = ""

        try:
            while time.time() - start < timeout:
                if process.poll() is not None:
                    rest = process.stdout.read()
                    if rest:
                        if artifact:
                            artifact.write(rest)
                        buf += rest.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                if artifact:
                    artifact.write(chunk)
                    artifact.flush()
                buf += chunk.decode("utf-8", errors="replace")

                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool = cb.get("name", "")
                                if tool == "Skill":
                                    pending_tool = tool
                                    accumulated = ""
                                else:
                                    pending_tool = None

                        elif se_type == "content_block_delta" and pending_tool:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated += delta.get("partial_json", "")
                                if skill_name in accumulated:
                                    return True

                        # message_stop fires after each assistant turn, not just
                        # the last one — don't exit here, wait for the result event.

                    elif event.get("type") == "assistant":
                        msg = event.get("message", {})
                        # Partial messages (stop_reason: null) arrive mid-stream
                        # before the tool call — skip them and let stream_event
                        # detection handle it. Only use this as a fallback when
                        # the message is complete.
                        if msg.get("stop_reason") is None:
                            continue
                        for item in msg.get("content", []):
                            if item.get("type") == "tool_use" and item.get("name") == "Skill":
                                if skill_name in item.get("input", {}).get("skill", ""):
                                    triggered = True
                        return triggered

                    elif event.get("type") == "result":
                        return triggered  # conversation over — True if Skill was invoked

        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            if artifact:
                artifact.close()

        return triggered

    finally:
        shutil.rmtree(tmp_config, ignore_errors=True)


@pytest.mark.trigger
def test_trigger_eval(trigger_case, tmp_path):
    """Skill triggers (or not) as expected for the given query."""
    result = _run_trigger_query(
        query=trigger_case.query,
        skill_path=trigger_case.skill_path,
        skill_name=trigger_case.skill_name,
        artifacts_dir=tmp_path,
    )
    direction = "trigger" if trigger_case.should_trigger else "NOT trigger"
    assert result == trigger_case.should_trigger, (
        f"Expected '{trigger_case.skill_name}' to {direction} for:\n"
        f"  {trigger_case.query!r}"
    )
