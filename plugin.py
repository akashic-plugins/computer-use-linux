from __future__ import annotations

from agent.plugins import McpServerSpec, Plugin


_PORTAL_ENV = {
    "COMPUTER_USE_LINUX_FORCE_PORTAL_POINTER": "1",
    "COMPUTER_USE_LINUX_FORCE_PORTAL_KEYBOARD": "1",
}


class ComputerUseLinuxPlugin(Plugin):
    name = "computer-use-linux"
    version = "1.0.1"
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
                command=("bash", "mcp/run.sh"),
                env=dict(_PORTAL_ENV),
            )
        ]
