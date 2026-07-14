from __future__ import annotations

from pathlib import Path

import pytest

import plugin
from plugin import ComputerUseLinuxPlugin


def _make_executable(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    _ = path.chmod(0o755)
    return path


def test_plugin_declares_skill_and_portal_mcp(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    binary = _make_executable(tmp_path / "computer-use-linux")
    monkeypatch.setenv("COMPUTER_USE_LINUX_BIN", str(binary))

    assert ComputerUseLinuxPlugin.skill_roots() == ("skills",)
    servers = ComputerUseLinuxPlugin.mcp_servers()
    assert len(servers) == 1
    assert servers[0].name == "computer-use-linux"
    assert servers[0].command == (str(binary.resolve()), "mcp")
    assert servers[0].env == {
        "COMPUTER_USE_LINUX_FORCE_PORTAL_POINTER": "1",
        "COMPUTER_USE_LINUX_FORCE_PORTAL_KEYBOARD": "1",
    }


def test_resolver_uses_highest_nvm_version(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    lower = _make_executable(
        tmp_path / ".nvm/versions/node/v9.1.0/bin/computer-use-linux"
    )
    higher = _make_executable(
        tmp_path / ".nvm/versions/node/v20.19.4/bin/computer-use-linux"
    )
    monkeypatch.delenv("COMPUTER_USE_LINUX_BIN", raising=False)
    monkeypatch.setattr(plugin.shutil, "which", lambda _: None)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    assert plugin._resolve_binary() == str(higher.resolve())
    assert plugin._resolve_binary() != str(lower.resolve())


def test_resolver_fails_loud_when_binary_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("COMPUTER_USE_LINUX_BIN", raising=False)
    monkeypatch.setattr(plugin.shutil, "which", lambda _: None)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    with pytest.raises(FileNotFoundError, match="未找到 computer-use-linux"):
        plugin._resolve_binary()


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
