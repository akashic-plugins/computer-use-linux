from __future__ import annotations

import json
import subprocess
from pathlib import Path

from plugin import ComputerUseLinuxPlugin


def test_plugin_declares_skill_and_autodetected_mcp() -> None:
    assert ComputerUseLinuxPlugin.skill_roots() == ("skills",)
    servers = ComputerUseLinuxPlugin.mcp_servers()
    assert len(servers) == 1
    assert servers[0].name == "computer-use-linux"
    assert servers[0].command == ("bash", "mcp/run.sh")
    assert servers[0].env == {}


def test_wrapper_forwards_mcp_protocol_to_explicit_binary(tmp_path: Path) -> None:
    server = tmp_path / "server.py"
    server.write_text(
        "#!/usr/bin/env python3\n"
        "import json, sys\n"
        "for line in sys.stdin:\n"
        "    request = json.loads(line)\n"
        "    result = {'protocolVersion': '2025-11-25'} if request['method'] == 'initialize' else {'tools': [{'name': 'doctor', 'inputSchema': {'type': 'object'}}]}\n"
        "    print(json.dumps({'jsonrpc': '2.0', 'id': request['id'], 'result': result}), flush=True)\n",
        encoding="utf-8",
    )
    _ = server.chmod(0o755)
    wrapper = Path(__file__).resolve().parents[1] / "mcp/run.sh"
    process = subprocess.Popen(
        ["bash", str(wrapper)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={"COMPUTER_USE_LINUX_BIN": str(server), "PATH": "/usr/bin"},
    )
    requests = (
        '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n'
        '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n'
    )
    stdout, stderr = process.communicate(requests, timeout=5)
    responses = [json.loads(line) for line in stdout.splitlines()]

    assert process.returncode == 0
    assert stderr == ""
    assert responses[0]["result"]["protocolVersion"] == "2025-11-25"
    assert responses[1]["result"]["tools"][0]["name"] == "doctor"


def test_wrapper_fails_loud_when_binary_is_missing(tmp_path: Path) -> None:
    wrapper = Path(__file__).resolve().parents[1] / "mcp/run.sh"
    result = subprocess.run(
        ["bash", str(wrapper)],
        capture_output=True,
        text=True,
        env={"HOME": str(tmp_path), "PATH": "/usr/bin"},
        check=False,
    )

    assert result.returncode == 127
    assert "未找到 computer-use-linux" in result.stderr


def test_skill_requires_readback_and_forbids_fake_success() -> None:
    skill = (
        Path(__file__).resolve().parents[1]
        / "skills/computer-use-linux/SKILL.md"
    ).read_text(encoding="utf-8")

    assert "read back" in skill
    assert "Report success only when the readback proves" in skill
    assert "Never create a shim or fallback that returns exit code 0" in skill
    assert "do not self-register another copy" in skill.lower()
    assert "never retry against whichever window is currently focused" in skill.lower()


def test_skill_covers_observed_wayland_and_browser_failures() -> None:
    skill = (
        Path(__file__).resolve().parents[1]
        / "skills/computer-use-linux/SKILL.md"
    ).read_text(encoding="utf-8")

    assert "coordinate_width" in skill
    assert "Do not multiply or divide" in skill
    assert "Screenshot portal readiness and RemoteDesktop input support are independent" in skill
    assert "Do not kill or restart the browser" in skill
    assert "hard-code `--user-data-dir`" in skill
    assert "use semantic elements when the tree is complete" in skill
    assert "add only `--force-renderer-accessibility`" in skill
    assert "never use `--restart` or a forced kill" in skill
    assert "Never bypass the MCP with raw `ydotool`" in skill
    assert "`ok=true` means only" in skill
