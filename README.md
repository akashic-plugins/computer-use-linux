# computer-use-linux for Akashic

Akashic plugin that contributes one `computer-use-linux` MCP server and one matching desktop-operation skill.

The host must already have `@agent-sh/computer-use-linux` installed. The plugin resolves the executable from `COMPUTER_USE_LINUX_BIN`, `PATH`, or the highest installed nvm Node version, and fails startup clearly when none exists.

```bash
python main.py plugin-install \
  --source https://github.com/akashic-plugins/computer-use-linux.git \
  --marketplace github
```

The MCP server auto-detects the available pointer and keyboard backends instead of forcing a portal implementation. The skill requires semantic targeting, screenshot-metadata coordinates, serialized mutations, browser-profile preservation, and observation-based readback before reporting success.
