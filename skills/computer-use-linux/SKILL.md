---
name: computer-use-linux
description: Use when Akashic needs to inspect or control the local Linux desktop through computer-use-linux, including browser tasks, accessibility trees, windows, screenshots, clicks, scrolling, text or key input, Wayland or Hyprland coordinate handling, and diagnosis of failed desktop actions.
---

# Computer Use Linux

Use the plugin-provided `computer-use-linux` MCP tools. The plugin owns MCP registration; do not add, replace, or remove workspace MCP declarations for this server.

## Core workflow

1. Use `tool_search` at most once to load only the required tools. Skip it when the tool is already callable; never search again after a successful call proves that it is loaded.
2. Run `doctor` once at the start of a desktop task, or again only after the backend environment actually changes. Treat its raw readiness fields and errors as evidence.
3. Use `list_windows` or `focused_window`, then bind every mutation to the intended window by id, pid, app id, title, or wm class.
4. Observe with `get_app_state`. Prefer a current element index or unique semantic selector; use coordinates only when the current accessibility tree has no usable target.
5. Execute one mutation at a time. After every click, key press, text entry, drag, scroll, action, or value change, read back the relevant state before continuing.

`ok=true` means only that an input backend accepted the action. Report success only when the readback proves the requested UI effect. Never run desktop mutations concurrently.

## Targeting and coordinates

- Treat MCP screenshot metadata as the coordinate authority. For a window-targeted screenshot, pass `relative=true` coordinates in its `coordinate_width` by `coordinate_height` space. Do not multiply or divide them by the compositor scale.
- A `grim` image uses physical output pixels and is not interchangeable with an MCP window screenshot. Prefer semantic targeting, keyboard navigation, or a fresh MCP screenshot. If an external screenshot is unavoidable, first read the live monitor scale and window geometry and explicitly convert both origin and size.
- Never reuse a coordinate after navigation, resize, scroll, a modal opening, or another layout change.
- For a standard modal whose intended button already has focus, prefer targeted `Enter` or `Escape` over an estimated click.
- An unchanged screenshot does not prove Wayland or portal isolation. First test whether the calculated target was correct and preserve the backend's raw result.

## Text and browser tasks

- Focus the explicit target window before keyboard input. Treat a `no focused element` warning as failed verification even if the keystrokes may have been sent.
- Prefer `set_value`, an editable element, or targeted `type_text`. For non-ASCII text, read back the exact text before sending; if the backend cannot enter it, report that limitation instead of invoking `ydotool` directly.
- Preserve an existing browser process and profile. Navigate in the current window with `Ctrl+L`, targeted text input, and `Enter` when the user authorizes navigation.
- Chromium or Electron may need `--force-renderer-accessibility` when the page tree is incomplete. Do not kill or restart the browser, hard-code `--user-data-dir` or `--profile-directory`, create a wrapper, or alter its DBus/keyring environment merely to enable the tree. Explain the limitation and ask the user to close and reopen normally before changing launch configuration.
- Never infer authentication from a homepage or the presence of cookie files. Verify with a protected page or an account control visible in the current UI.

## Backend diagnosis

- Let `computer-use-linux` auto-detect pointer and keyboard backends. Screenshot portal readiness and RemoteDesktop input support are independent; a working Hyprland screenshot portal does not prove portal pointer or keyboard support.
- Preserve the original error and distinguish `EPERM`, `EACCES`, `EINVAL`, missing executable, timeout, unsupported backend, and a stale target. Do not rewrite one as another.
- After one failed action, make one observation that can distinguish the suspected causes. Retry only once and only when that observation changes the target or backend assumption.
- Do not install packages, start services, change groups or ACLs, edit launchers, browser profiles, plugin configuration, or MCP configuration unless the user explicitly authorizes that system change. Query the installed package and unit names before recommending a service command.

## Failure boundaries

- Never create a shim or fallback that returns exit code 0 without performing the action.
- Never bypass the MCP with raw `ydotool`, `xdotool`, or shell-driven input. Do not wander into unrelated installers, repositories, input libraries, or speculative portal repairs.
- Treat the user's requested desktop action as the authorization boundary. Sending, submitting, deleting, purchasing, overwriting, closing an application, or restarting a process requires authorization from the request or a new confirmation.
- If a window or element target becomes stale, stop with that error; never retry against whichever window is currently focused.
- If the MCP tools are absent, report that the `computer-use-linux` plugin is not active in this turn and ask for plugin status/restart verification. Do not self-register another copy.

## Capability guide

- Observe: `doctor`, `list_windows`, `list_apps`, `focused_window`, `get_app_state`, `screenshot`.
- Target/focus: `activate_window` plus window selectors.
- Mutate: `click`, `drag`, `scroll`, `press_key`, `type_text`, `perform_action`, `set_value`.

Desktop input is real and stateful. Keep the action set limited to the user's request and do not claim completion from a tool's exit status alone.
