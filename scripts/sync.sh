#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly AGENTS_FILE="$REPO_DIR/AGENTS.md"
readonly SKILLS_DIR="$REPO_DIR/skills"

usage() {
  cat <<'EOF'
Usage: sync.sh <claude|codex|cursor|all>

Symlink the canonical instructions and repository skills for the selected AI tool.
EOF
}

tool_skills_path() {
  case "$1" in
    claude) printf '%s\n' "$HOME/.claude/skills" ;;
    codex) printf '%s\n' "$HOME/.agents/skills" ;;
    cursor) printf '%s\n' "$HOME/.cursor/skills" ;;
  esac
}

tool_instructions_path() {
  case "$1" in
    claude) printf '%s\n' "$HOME/.claude/CLAUDE.md" ;;
    codex) printf '%s\n' "$HOME/.codex/AGENTS.md" ;;
    cursor) printf '%s\n' "$HOME/.cursor/rules/AGENTS.mdc" ;;
  esac
}

tool_available() {
  case "$1" in
    claude) command -v claude >/dev/null 2>&1 ;;
    codex) command -v codex >/dev/null 2>&1 ;;
    cursor)
      command -v cursor >/dev/null 2>&1 ||
        [[ -d /Applications/Cursor.app ]] ||
        [[ -d "$HOME/Applications/Cursor.app" ]]
      ;;
  esac
}

skill_sources() {
  local skill

  for skill in "$SKILLS_DIR"/*; do
    [[ -d "$skill" ]] && printf '%s\n' "$skill"
  done
}

sync_target() {
  local source="$1"
  local target="$2"
  local target_dir

  target_dir="$(dirname "$target")"

  if [[ -e "$target_dir" && ! -d "$target_dir" ]]; then
    printf 'Conflict: %s is not a directory\n' "$target_dir" >&2
    return 1
  fi

  if [[ -L "$target" && "$(readlink "$target")" == "$source" ]]; then
    return 0
  fi

  if [[ -e "$target" || -L "$target" ]]; then
    printf 'Conflict: %s already exists\n' "$target" >&2
    return 1
  fi

  if [[ ! -d "$target_dir" ]]; then
    printf 'Create: %s\n' "$target_dir"
    mkdir -p "$target_dir"
  fi

  printf 'Link: %s -> %s\n' "$target" "$source"
  ln -s "$source" "$target"
}

sync_tool() {
  local tool="$1"
  local skills_dir
  local source
  local has_conflict=0

  if ! sync_target "$AGENTS_FILE" "$(tool_instructions_path "$tool")"; then
    has_conflict=1
  fi

  skills_dir="$(tool_skills_path "$tool")"

  while IFS= read -r source; do
    if ! sync_target "$source" "$skills_dir/${source##*/}"; then
      has_conflict=1
    fi
  done < <(skill_sources)

  return "$has_conflict"
}

main() {
  local selection="${1:-help}"
  local tools=()
  local candidates=()
  local tool
  local has_conflict=0

  case "$selection" in
    claude|codex|cursor) tools=("$selection") ;;
    all)
      candidates=(claude codex cursor)

      for tool in "${candidates[@]}"; do
        tool_available "$tool" && tools+=("$tool")
      done

      if ((${#tools[@]} == 0)); then
        printf 'Error: no supported AI tool detected\n' >&2
        return 1
      fi
      ;;
    help|-h|--help)
      usage
      return 0
      ;;
    *)
      usage >&2
      return 2
      ;;
  esac

  if [[ ! -f "$AGENTS_FILE" ]]; then
    printf 'Error: canonical instructions not found: %s\n' "$AGENTS_FILE" >&2
    return 1
  fi

  if [[ ! -d "$SKILLS_DIR" ]]; then
    printf 'Error: skills directory not found: %s\n' "$SKILLS_DIR" >&2
    return 1
  fi

  for tool in "${tools[@]}"; do
    if ! sync_tool "$tool"; then
      has_conflict=1
    fi
  done

  return "$has_conflict"
}

main "$@"
