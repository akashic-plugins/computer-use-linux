---
name: computer-use-linux
description: Use when Akashic needs to inspect or control the local Linux desktop through computer-use-linux, including reading windows or accessibility state, focusing apps, screenshots, clicks, scrolling, typing, key presses, or diagnosing a failed desktop action.
---

# Computer Use Linux

Use the plugin-provided `computer-use-linux` MCP tools. The plugin owns MCP registration; do not add, replace, or remove workspace MCP declarations for this server.

## Operating procedure

1. Use `tool_search` once to load the smallest set of `computer-use-linux` tools required for the current task.
2. Start a desktop-control task with `doctor`. Treat its raw readiness fields and errors as evidence; do not infer permissions from Unix owner/group text alone.
3. Call `list_windows` or `focused_window`, then identify the intended window by title, app id, pid, or wm class.
4. Prefer semantic targets from `get_app_state`, such as element index, role, name, text, or states. Use coordinates only when the accessibility tree has no useful target.
5. Execute one state-changing action at a time. Never run desktop mutations concurrently.
6. After every click, key press, text entry, drag, scroll, action, or value change, read back with `get_app_state`, `focused_window`, or another relevant observation. Report success only when the readback proves the requested effect.

For text entry, use an explicit window target whenever the tool supports one. Focus the target window before keyboard input. On Hyprland, the plugin forces the desktop portal for pointer and keyboard input; a portal prompt or backend error is not permission to switch implementations.

Treat the user's requested desktop action as the authorization boundary. Ask before adding unrelated destructive actions. If an explicit window or element target becomes stale, stop with that error; never retry against whichever window is currently focused.

## Failure boundaries

- Preserve the original error and distinguish `EPERM`, `EACCES`, `EINVAL`, missing executable, timeout, and unsupported backend. Never rewrite one as another.
- Do not install packages, compile source, change groups or ACLs, start services, edit MCP configuration, or create replacement executables unless the user explicitly asks for that system change.
- Never create a shim or fallback that returns exit code 0 without performing the action.
- After one documented tool/backend attempt fails, make at most one safe observation to diagnose it, then stop and report the raw blocker. Do not wander into unrelated installers, repositories, or input libraries.
- If the MCP tools are absent, report that the `computer-use-linux` plugin is not active in this turn and ask for plugin status/restart verification. Do not self-register another copy.

## Capability guide

- Observe: `doctor`, `list_windows`, `list_apps`, `focused_window`, `get_app_state`, `screenshot`.
- Target/focus: `activate_window` plus window selectors.
- Mutate: `click`, `drag`, `scroll`, `press_key`, `type_text`, `perform_action`, `set_value`.

Desktop input is real and stateful. Keep the action set limited to the user's request and do not claim completion from a tool's exit status alone.
