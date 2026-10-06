#!/usr/bin/env bash

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly AGENTS_FILE="$REPO_DIR/AGENTS.md"
readonly SKILLS_DIR="$REPO_DIR/skills"

usage() {
  cat <<'EOF'
Usage: sync.sh <claude|codex|cursor|all>
       sync.sh remove <skill-name> [claude|codex|cursor|all]

Install canonical instructions and repository skills for the selected AI tool.
Managed nemo-* skill symlinks and instruction links that already point inside this
repository are repointed when the source path changes. Foreign files stay conflicts.
Stale managed nemo-* symlinks that point into this repo but no longer have a skill
source are removed during sync.
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
        [[ -d "$HOME/.cursor" ]] ||
        [[ -d /Applications/Cursor.app ]] ||
        [[ -d "$HOME/Applications/Cursor.app" ]]
      ;;
  esac
}

skill_sources() {
  local skill

  for skill in "$SKILLS_DIR"/nemo-*; do
    [[ -f "$skill/SKILL.md" ]] && printf '%s\n' "$skill"
  done
}

prune_stale_skills() {
  local skills_dir="$1"
  local entry current name

  [[ -d "$skills_dir" ]] || return 0

  for entry in "$skills_dir"/nemo-*; do
    [[ -L "$entry" ]] || continue
    current="$(readlink "$entry")"
    name="${entry##*/}"
    [[ "$current" == "$SKILLS_DIR"/* ]] || continue
    if [[ -f "$SKILLS_DIR/$name/SKILL.md" && -e "$entry" ]]; then
      continue
    fi
    printf 'Remove: %s (stale managed skill)\n' "$entry"
    rm -f "$entry"
  done
}

remove_managed_skill() {
  local name="$1"
  local tool="$2"
  local target

  case "$name" in
    nemo-*) ;;
    *)
      printf 'Error: only managed nemo-* skill names can be removed\n' >&2
      return 2
      ;;
  esac

  target="$(tool_skills_path "$tool")/$name"
  if [[ -L "$target" && "$(readlink "$target")" == "$SKILLS_DIR"/* ]]; then
    printf 'Remove: %s\n' "$target"
    rm -f "$target"
    return 0
  fi
  if [[ -e "$target" || -L "$target" ]]; then
    printf 'Conflict: %s is not a managed skill link\n' "$target" >&2
    return 1
  fi
  return 0
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

  if [[ -L "$target" ]]; then
    if [[ "$(readlink "$target")" == "$source" ]]; then
      return 0
    fi
    # Repoint only managed links that already point inside this repository.
    if [[ "$(readlink "$target")" == "$REPO_DIR"/* ]]; then
      if [[ "$source" == "$SKILLS_DIR"/nemo-* && "$(basename "$target")" == "$(basename "$source")" ]] ||
         [[ "$source" == "$AGENTS_FILE" ]]; then
        printf 'Relink: %s -> %s\n' "$target" "$source"
        ln -sfn "$source" "$target"
        return 0
      fi
    fi
    printf 'Conflict: %s already exists\n' "$target" >&2
    return 1
  fi

  if [[ -e "$target" ]]; then
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

sync_cursor_instructions() {
  local target="$1"
  local target_dir
  local expected
  local temporary

  target_dir="$(dirname "$target")"
  expected="$(printf '%s\n' '---' 'alwaysApply: true' '---' '' \
    "Read and follow [the global agent rules](<$AGENTS_FILE>) before working.")"

  if [[ -L "$target" ]]; then
    if [[ "$(readlink "$target")" != "$AGENTS_FILE" ]]; then
      printf 'Conflict: %s points to another instruction source\n' "$target" >&2
      return 1
    fi
  elif [[ -f "$target" && "$(cat "$target")" == "$expected" ]]; then
    return 0
  elif [[ -e "$target" ]]; then
    printf 'Conflict: %s already exists\n' "$target" >&2
    return 1
  fi
  if [[ -e "$target_dir" && ! -d "$target_dir" ]]; then
    printf 'Conflict: %s is not a directory\n' "$target_dir" >&2
    return 1
  fi

  mkdir -p "$target_dir"
  temporary="$(mktemp "$target_dir/.nemo-rule.XXXXXX")"
  if ! printf '%s\n' "$expected" > "$temporary" || ! mv -f "$temporary" "$target"; then
    rm -f "$temporary"
    return 1
  fi
  printf 'Rule: %s -> %s\n' "$target" "$AGENTS_FILE"
}

sync_tool() {
  local tool="$1"
  local skills_dir
  local source
  local has_conflict=0

  if [[ "$tool" == cursor ]]; then
    if ! sync_cursor_instructions "$(tool_instructions_path "$tool")"; then
      has_conflict=1
    fi
  elif ! sync_target "$AGENTS_FILE" "$(tool_instructions_path "$tool")"; then
    has_conflict=1
  fi

  skills_dir="$(tool_skills_path "$tool")"
  prune_stale_skills "$skills_dir"

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
  local remove_scope

  case "$selection" in
    remove)
      if [[ -z "${2:-}" ]]; then
        usage >&2
        return 2
      fi
      remove_scope="${3:-all}"
      case "$remove_scope" in
        claude|codex|cursor) tools=("$remove_scope") ;;
        all)
          for tool in claude codex cursor; do
            tool_available "$tool" && tools+=("$tool")
          done
          ;;
        *)
          usage >&2
          return 2
          ;;
      esac
      if ((${#tools[@]} == 0)); then
        printf 'Error: no supported AI tool detected\n' >&2
        return 1
      fi
      for tool in "${tools[@]}"; do
        if ! remove_managed_skill "$2" "$tool"; then
          has_conflict=1
        fi
      done
      return "$has_conflict"
      ;;
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
