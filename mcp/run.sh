#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

if [[ -n "${COMPUTER_USE_LINUX_BIN:-}" ]]; then
  if [[ ! -x "$COMPUTER_USE_LINUX_BIN" ]]; then
    echo "COMPUTER_USE_LINUX_BIN 不可执行: $COMPUTER_USE_LINUX_BIN" >&2
    exit 127
  fi
  exec "$COMPUTER_USE_LINUX_BIN" mcp
fi

if command -v computer-use-linux >/dev/null 2>&1; then
  exec computer-use-linux mcp
fi

nvm_root="${NVM_DIR:-$HOME/.nvm}/versions/node"
launcher="$({
  for candidate in "$nvm_root"/v*/bin/computer-use-linux; do
    [[ -x "$candidate" ]] && printf '%s\n' "$candidate"
  done
  true
} | sort -V | tail -n 1)"

if [[ -z "$launcher" ]]; then
  echo "未找到 computer-use-linux；请先安装 @agent-sh/computer-use-linux，或设置 COMPUTER_USE_LINUX_BIN" >&2
  exit 127
fi

node="$(dirname "$launcher")/node"
if [[ ! -x "$node" ]]; then
  echo "computer-use-linux 对应的 Node 不可执行: $node" >&2
  exit 127
fi

exec "$node" "$(readlink -f "$launcher")" mcp
