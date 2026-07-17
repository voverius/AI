#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly SKILLS_DIR="$REPO_DIR/skills"

usage() {
  cat <<'EOF'
Usage: sync.sh <claude|codex|cursor|all>

Symlink repository skills into the selected tool's user-level skills directory.
EOF
}

tool_path() {
  case "$1" in
    claude) printf '%s\n' "$HOME/.claude/skills" ;;
    codex) printf '%s\n' "$HOME/.agents/skills" ;;
    cursor) printf '%s\n' "$HOME/.cursor/skills" ;;
  esac
}

skill_sources() {
  local skill

  for skill in "$SKILLS_DIR"/*; do
    [[ -d "$skill" ]] && printf '%s\n' "$skill"
  done
}

preflight_tool() {
  local tool="$1"
  local target_dir
  local source
  local target
  local has_conflict=0

  target_dir="$(tool_path "$tool")"

  if [[ -e "$target_dir" && ! -d "$target_dir" ]]; then
    printf 'Conflict: %s is not a directory\n' "$target_dir" >&2
    return 1
  fi

  while IFS= read -r source; do
    target="$target_dir/${source##*/}"

    if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
      continue
    fi

    if [[ -e "$target" || -L "$target" ]]; then
      printf 'Conflict: %s already exists\n' "$target" >&2
      has_conflict=1
    fi
  done < <(skill_sources)

  ((has_conflict == 0))
}

sync_tool() {
  local tool="$1"
  local target_dir
  local source
  local target

  target_dir="$(tool_path "$tool")"

  if [[ ! -d "$target_dir" ]]; then
    printf 'Create: %s\n' "$target_dir"
    mkdir -p "$target_dir"
  fi

  while IFS= read -r source; do
    target="$target_dir/${source##*/}"

    if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
      printf 'Unchanged: %s\n' "$target"
      continue
    fi

    printf 'Link: %s -> %s\n' "$target" "$source"
    ln -s "$source" "$target"
  done < <(skill_sources)
}

main() {
  local selection="${1:-help}"
  local tools=()
  local tool

  case "$selection" in
    claude|codex|cursor) tools=("$selection") ;;
    all) tools=(claude codex cursor) ;;
    help|-h|--help)
      usage
      return 0
      ;;
    *)
      usage >&2
      return 2
      ;;
  esac

  if [[ ! -d "$SKILLS_DIR" ]]; then
    printf 'Error: skills directory not found: %s\n' "$SKILLS_DIR" >&2
    return 1
  fi

  for tool in "${tools[@]}"; do
    preflight_tool "$tool"
  done

  for tool in "${tools[@]}"; do
    sync_tool "$tool"
  done
}

main "$@"
