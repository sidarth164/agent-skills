#!/usr/bin/env bash
# Removes symlinks in ~/.claude/skills/ that point into this repo.
# Does NOT delete any actual skill files.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DST="$HOME/.claude/skills"

usage() {
  cat <<EOF
Usage: $(basename "$0") [skill-name ...]

Removes symlinks in ~/.claude/skills/ that point into this repo.

  $(basename "$0")                       # uninstall all
  $(basename "$0") mcp-builder           # uninstall just mcp-builder
  $(basename "$0") -h                    # show this help
EOF
}

uninstall_skill() {
  local skill_name="$1"
  local target="$SKILLS_DST/$skill_name"

  if [ ! -L "$target" ]; then
    echo "  skip: $skill_name (not a symlink or not installed)" >&2
    return 1
  fi

  local existing
  existing="$(readlink "$target")"
  case "$existing" in
    "$REPO_DIR"/skills/*)
      rm "$target"
      echo "  removed: $skill_name"
      ;;
    *)
      echo "  skip: $skill_name (symlink does not point to this repo)" >&2
      return 1
      ;;
  esac
}

main() {
  if [[ "${1:-}" =~ ^-*h(elp)?$ ]]; then
    usage
    exit 0
  fi

  local skills=()
  if [ $# -eq 0 ]; then
    # Collect all symlinks in SKILLS_DST that point into this repo
    for link in "$SKILLS_DST"/*/; do
      [ -L "${link%/}" ] || continue
      local t
      t="$(readlink "${link%/}")"
      case "$t" in
        "$REPO_DIR"/skills/*) skills+=("$(basename "${link%/}")") ;;
      esac
    done
  else
    skills=("$@")
  fi

  if [ ${#skills[@]} -eq 0 ]; then
    echo "Nothing to uninstall."
    exit 0
  fi

  local ok=0
  local fail=0
  for skill in "${skills[@]}"; do
    if uninstall_skill "$skill"; then
      ok=$((ok + 1))
    else
      fail=$((fail + 1))
    fi
  done

  echo ""
  echo "Done: $ok removed, $fail failed"
  if [ "$fail" -gt 0 ]; then exit 1; fi
}

main "$@"
