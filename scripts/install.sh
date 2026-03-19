#!/usr/bin/env bash
# Symlinks skills from this repo into ~/.claude/skills/.
# Safe to re-run — skips existing symlinks that already point here, warns on conflicts.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DST="$HOME/.claude/skills"

usage() {
  cat <<EOF
Usage: $(basename "$0") [skill-name ...]

Symlinks skills from this repo into ~/.claude/skills/.

  $(basename "$0")              # install all skills
  $(basename "$0") mcp-builder  # install just mcp-builder
  $(basename "$0") -h           # show this help
EOF
}

install_skill() {
  local skill_name="$1"
  local skill_dir="$SKILLS_SRC/$skill_name"
  local target="$SKILLS_DST/$skill_name"

  if [ ! -d "$skill_dir" ]; then
    echo "  ERROR: skill '$skill_name' not found in $SKILLS_SRC" >&2
    return 1
  fi

  if [ -L "$target" ]; then
    local existing
    existing="$(readlink "$target")"
    if [ "$existing" = "$skill_dir" ] || [ "$existing" = "$skill_dir/" ]; then
      echo "  skip: $skill_name (already linked)"
      return 0
    else
      echo "  CONFLICT: $skill_name -> $existing (not from this repo)" >&2
      return 1
    fi
  elif [ -e "$target" ]; then
    echo "  CONFLICT: $skill_name exists and is not a symlink" >&2
    return 1
  fi

  ln -s "$skill_dir" "$target"
  echo "  linked: $skill_name"
}

main() {
  if [[ "${1:-}" =~ ^-*h(elp)?$ ]]; then
    usage
    exit 0
  fi

  mkdir -p "$SKILLS_DST"

  local skills=()
  if [ $# -eq 0 ]; then
    for d in "$SKILLS_SRC"/*/; do
      [ -d "$d" ] && skills+=("$(basename "$d")")
    done
  else
    skills=("$@")
  fi

  local ok=0
  local fail=0
  for skill in "${skills[@]}"; do
    if install_skill "$skill"; then
      ok=$((ok + 1))
    else
      fail=$((fail + 1))
    fi
  done

  echo ""
  echo "Done: $ok ok, $fail failed"
  if [ "$fail" -gt 0 ]; then exit 1; fi
}

main "$@"
