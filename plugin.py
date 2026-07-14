from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from agent.plugins import McpServerSpec, Plugin


_PORTAL_ENV = {
    "COMPUTER_USE_LINUX_FORCE_PORTAL_POINTER": "1",
    "COMPUTER_USE_LINUX_FORCE_PORTAL_KEYBOARD": "1",
}


class ComputerUseLinuxPlugin(Plugin):
    name = "computer-use-linux"
    version = "1.0.0"
    desc = "Linux desktop control MCP and operating skill"
    author = "akashic-plugins"

    @classmethod
    def skill_roots(cls) -> tuple[str, ...]:
        return ("skills",)

    @classmethod
    def mcp_servers(cls) -> list[McpServerSpec]:
        return [
            McpServerSpec(
                name="computer-use-linux",
                command=(_resolve_binary(), "mcp"),
                env=dict(_PORTAL_ENV),
            )
        ]


def _resolve_binary() -> str:
    """解析已安装的 computer-use-linux，并在缺失时明确失败。"""

    # 1. 优先使用显式配置和当前进程 PATH。
    override = os.environ.get("COMPUTER_USE_LINUX_BIN", "").strip()
    if override:
        return _require_executable(Path(override))
    discovered = shutil.which("computer-use-linux")
    if discovered:
        return _require_executable(Path(discovered))

    # 2. systemd 用户服务常不继承 nvm PATH，选择已安装的最高 Node 版本。
    candidates = list(
        (Path.home() / ".nvm" / "versions" / "node").glob(
            "v*/bin/computer-use-linux"
        )
    )
    if candidates:
        selected = max(candidates, key=_node_version)
        return _require_executable(selected)
    raise FileNotFoundError(
        "未找到 computer-use-linux；请先安装 @agent-sh/computer-use-linux，"
        "或设置 COMPUTER_USE_LINUX_BIN"
    )


def _node_version(path: Path) -> tuple[int, ...]:
    match = re.fullmatch(r"v(\d+(?:\.\d+)*)", path.parents[1].name)
    if match is None:
        raise ValueError(f"无法解析 Node 版本目录: {path.parents[1]}")
    return tuple(int(part) for part in match.group(1).split("."))


def _require_executable(path: Path) -> str:
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise PermissionError(f"computer-use-linux 不可执行: {resolved}")
    return str(resolved)
