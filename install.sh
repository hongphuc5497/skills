#!/usr/bin/env bash
set -euo pipefail

# ─── ANSI colors (with dumb-terminal fallback) ─────────────────────────────
if [[ "${TERM:-dumb}" != "dumb" ]] && command -v tput &>/dev/null && tput colors &>/dev/null; then
  BOLD=$(tput bold)    DIM=$(tput dim)      RESET=$(tput sgr0)
  GREEN=$(tput setaf 2) CYAN=$(tput setaf 6) YELLOW=$(tput setaf 3) RED=$(tput setaf 1)
else
  BOLD="" DIM="" RESET="" GREEN="" CYAN="" YELLOW="" RED="" RESET=""
fi

# ─── Restore terminal on unexpected exit ────────────────────────────────────
cleanup() { stty echo icanon 2>/dev/null || true; tput cnorm 2>/dev/null || true; }
trap cleanup EXIT

# ─── Globals ────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS=""
SKILLS=()           # discovered skill folder names
SKILL_DESCS=()      # one-line descriptions (from frontmatter)
SKILL_PATHS=()      # absolute source path per skill (parallel to SKILLS)
SKILL_SEL=()        # 1/0 toggle per skill
TOOLS=("Claude Code" "Cursor" "Windsurf" "GitHub Copilot" "OpenAI Codex" "OpenCode" "Goal: Your/ AI coding tool")
TOOL_SEL=()         # 1/0 toggle per tool
INSTALL_SCOPE=""    # "global" or "project"
INSTALLED=()        # log: "skill → tool → path"
INSTALL_ALL_TOOLS=0 # 1 if "Install All" was toggled for tools

# ─── OS detection ───────────────────────────────────────────────────────────
detect_os() {
  case "$(uname -s)" in
    Darwin*)  OS="macOS" ;;
    Linux*)
      if grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
        OS="WSL"
      else
        OS="Linux"
      fi ;;
    CYGWIN*|MINGW*|MSYS*) OS="Windows" ;;
    *) OS="Unknown" ;;
  esac
}

# ─── Discover skills (folders containing SKILL.md) ─────────────────────────
discover_skills() {
  local dir desc prev_nullglob
  prev_nullglob=$(shopt -p nullglob)
  shopt -s nullglob
  for dir in "$SCRIPT_DIR"/skills/*/ "$SCRIPT_DIR"/skills/*/*/; do
    [[ -f "$dir/SKILL.md" ]] || continue
    local name
    name="$(basename "$dir")"
    desc=$(awk '/^---$/{n++; next} n==1 && /^description:/{sub(/^description: *"?"?/, ""); sub(/"$/, ""); print; exit}' "$dir/SKILL.md")
    if [[ ${#desc} -gt 70 ]]; then
      desc="${desc:0:67}..."
    fi
    SKILLS+=("$name")
    SKILL_DESCS+=("$desc")
    SKILL_PATHS+=("$dir")
    SKILL_SEL+=(0)
  done
  eval "$prev_nullglob"
}

# ─── Tool paths by tool name ────────────────────────────────────────────────
get_tool_paths() {
  local tool="$1" scope="$2" gpath ppath
  case "$tool" in
    "Claude Code")
      gpath="$HOME/.claude/skills"
      ppath=".claude/skills" ;;
    "Cursor")
      gpath="$HOME/.agents/skills"
      ppath=".cursor/rules" ;;
    "Windsurf")
      gpath="$HOME/.agents/skills"
      ppath=".windsurf/rules" ;;
    "GitHub Copilot")
      gpath="$HOME/.agents/skills"
      ppath=".github/instructions" ;;
    "OpenAI Codex")
      gpath="$HOME/.codex/skills"
      ppath=".codex/skills" ;;
    "OpenCode")
      gpath="$HOME/.agents/skills"
      ppath=".opencode/skills" ;;
    *)
      gpath="$HOME/.agents/skills"
      ppath=".agents/skills" ;;
  esac
  if [[ "$scope" == "project" ]]; then
    echo "$ppath"
  else
    echo "$gpath"
  fi
}

# ─── Install one skill to one tool path ────────────────────────────────────
install_skill() {
  local skill="$1" tool="$2" dest_base="$3" src="$4"
  local dest="$dest_base/$skill"
  if [[ -d "$dest" ]]; then
    echo "  ${YELLOW}⚠${RESET} $skill already at $dest (skip)"
    return
  fi
  mkdir -p "$dest"
  # Copy all files from source except subdirectories that are themselves skills
  local item
  for item in "$src"/* "$src"/.*; do
    [[ -e "$item" ]] || continue
    local base
    base="$(basename "$item")"
    [[ "$base" == "." || "$base" == ".." ]] && continue
    # Skip skill subdirectories (they get installed independently)
    if [[ -d "$item" && -f "$item/SKILL.md" ]]; then
      continue
    fi
    cp -r "$item" "$dest/" 2>/dev/null || true
  done
  INSTALLED+=("$skill → $tool → $dest")
  echo "  ${GREEN}✓${RESET} $skill → $dest"
}

# ─── Full install loop ──────────────────────────────────────────────────────
run_install() {
  local scope="$1" sel_idx=0 skill tool_idx
  local dest_base
  for ((sel_idx=0; sel_idx<${#SKILLS[@]}; sel_idx++)); do
    [[ ${SKILL_SEL[$sel_idx]} -eq 1 ]] || continue
    local skill="${SKILLS[$sel_idx]}"
    local src="${SKILL_PATHS[$sel_idx]}"
    if [[ $INSTALL_ALL_TOOLS -eq 1 ]]; then
      for ((tool_idx=0; tool_idx<${#TOOLS[@]}; tool_idx++)); do
        dest_base=$(get_tool_paths "${TOOLS[$tool_idx]}" "$scope")
        install_skill "$skill" "${TOOLS[$tool_idx]}" "$dest_base" "$src"
      done
    else
      for ((tool_idx=0; tool_idx<${#TOOLS[@]}; tool_idx++)); do
        [[ ${TOOL_SEL[$tool_idx]} -eq 1 ]] || continue
        dest_base=$(get_tool_paths "${TOOLS[$tool_idx]}" "$scope")
        install_skill "$skill" "${TOOLS[$tool_idx]}" "$dest_base" "$src"
      done
    fi
  done
}

# ─── TUI: scope picker ──────────────────────────────────────────────────────
pick_scope() {
  echo
  echo "  ${BOLD}Install scope?${RESET}"
  echo "    ${BOLD}1${RESET}) Global  — install to ~/.agents/skills/ etc. (all projects)"
  echo "    ${BOLD}2${RESET}) Project — install to .claude/ etc. in current directory"
  echo
  while true; do
    read -rp "  Scope [1/2] (1): " choice </dev/tty
    choice="${choice:-1}"
    case "$choice" in
      1) INSTALL_SCOPE="global"; break ;;
      2) INSTALL_SCOPE="project"; break ;;
      *) echo "  ${RED}Invalid${RESET}" ;;
    esac
  done
}

# ─── TUI: skill picker (multi-select with arrows) ───────────────────────────
pick_skills() {
  local idx=0 key
  local rows cols line header_len
  rows=$(tput lines 2>/dev/null || echo 40)
  cols=$(tput cols 2>/dev/null || echo 80)
  header_len=8  # title + spacer + header
  tput civis 2>/dev/null || true
  while true; do
    echo -ne "\033[H\033[J" 2>/dev/null || clear
    echo "  ${BOLD}Select skills to install${RESET} (↑↓ navigate, Space toggle, Enter done)"
    echo
    printf "  %-4s %-30s %s\n" "" "SKILL" "DESCRIPTION"
    local i
    for ((i=0; i<${#SKILLS[@]}; i++)); do
      if [[ $i -eq $idx ]]; then
        if [[ ${SKILL_SEL[$i]} -eq 1 ]]; then
          printf "  ${GREEN}▶ [✓]${RESET} %-30s %s\n" "${SKILLS[$i]}" "${SKILL_DESCS[$i]}"
        else
          printf "  ${CYAN}▶ [ ]${RESET} %-30s %s\n" "${SKILLS[$i]}" "${SKILL_DESCS[$i]}"
        fi
      else
        if [[ ${SKILL_SEL[$i]} -eq 1 ]]; then
          printf "  ${GREEN}  [✓]${RESET} %-30s %s\n" "${SKILLS[$i]}" "${SKILL_DESCS[$i]}"
        else
          printf "  ${DIM}  [ ]${RESET} %-30s %s\n" "${SKILLS[$i]}" "${SKILL_DESCS[$i]}"
        fi
      fi
    done
    read -rsn1 key </dev/tty
    if [[ $key == $'\x1b' ]]; then
      read -rsn2 key </dev/tty
      case "$key" in
        "[A") ((idx = (idx - 1 + ${#SKILLS[@]}) % ${#SKILLS[@]})) ;;
        "[B") ((idx = (idx + 1) % ${#SKILLS[@]})) ;;
      esac
    elif [[ $key == " " ]]; then
      SKILL_SEL[$idx]=$(( 1 - SKILL_SEL[$idx] ))
    elif [[ $key == "" || $key == $'\n' ]]; then
      break
    fi
  done
  tput cnorm 2>/dev/null || true
  echo -ne "\033[H\033[J" 2>/dev/null || clear
}

# ─── TUI: tool picker (multi-select with checkboxes) ────────────────────────
pick_tools() {
  local idx=0 key
  tput civis 2>/dev/null || true
  while true; do
    echo -ne "\033[H\033[J" 2>/dev/null || clear
    echo "  ${BOLD}Select target tools${RESET} (↑↓ navigate, Space toggle, Enter done)"
    echo "  ${DIM}Install All${RESET} toggles every tool at once"
    echo
    # "Install All" toggle
    if [[ $idx -eq 0 ]]; then
      if [[ $INSTALL_ALL_TOOLS -eq 1 ]]; then
        echo "  ${GREEN}▶ [✓]${RESET} Install All"
      else
        echo "  ${CYAN}▶ [ ]${RESET} Install All"
      fi
    else
      if [[ $INSTALL_ALL_TOOLS -eq 1 ]]; then
        echo "  ${GREEN}  [✓]${RESET} Install All"
      else
        echo "  ${DIM}  [ ]${RESET} Install All"
      fi
    fi
    local i
    for ((i=0; i<${#TOOLS[@]}; i++)); do
      local display_idx=$((i + 1))
      if [[ $display_idx -eq $idx ]]; then
        if [[ ${TOOL_SEL[$i]} -eq 1 ]]; then
          printf "  ${GREEN}▶ [✓]${RESET} %s\n" "${TOOLS[$i]}"
        else
          printf "  ${CYAN}▶ [ ]${RESET} %s\n" "${TOOLS[$i]}"
        fi
      else
        if [[ ${TOOL_SEL[$i]} -eq 1 ]]; then
          printf "  ${GREEN}  [✓]${RESET} %s\n" "${TOOLS[$i]}"
        else
          printf "  ${DIM}  [ ]${RESET} %s\n" "${TOOLS[$i]}"
        fi
      fi
    done
    read -rsn1 key </dev/tty
    if [[ $key == $'\x1b' ]]; then
      read -rsn2 key </dev/tty
      case "$key" in
        "[A") ((idx = (idx - 1 + ${#TOOLS[@]} + 1) % (${#TOOLS[@]} + 1))) ;;
        "[B") ((idx = (idx + 1) % (${#TOOLS[@]} + 1))) ;;
      esac
    elif [[ $key == " " ]]; then
      if [[ $idx -eq 0 ]]; then
        INSTALL_ALL_TOOLS=$(( 1 - INSTALL_ALL_TOOLS ))
      else
        local tidx=$((idx - 1))
        TOOL_SEL[$tidx]=$(( 1 - TOOL_SEL[$tidx] ))
      fi
    elif [[ $key == "" || $key == $'\n' ]]; then
      break
    fi
  done
  tput cnorm 2>/dev/null || true
}

# ─── Summary ────────────────────────────────────────────────────────────────
print_summary() {
  echo
  echo "  ${BOLD}Installation Summary${RESET}"
  echo "  ${DIM}────────────────────────────${RESET}"
  local entry
  for entry in "${INSTALLED[@]}"; do
    echo "  ${GREEN}✓${RESET} $entry"
  done
  echo
  if [[ ${#INSTALLED[@]} -eq 0 ]]; then
    echo "  ${YELLOW}Nothing installed.${RESET}"
  fi
}

# ─── Main ───────────────────────────────────────────────────────────────────
main() {
  detect_os
  echo
  echo "  ${BOLD}${CYAN}╔══════════════════════════════════════════╗${RESET}"
  echo "  ${BOLD}${CYAN}║   Agent Skills Installer                 ║${RESET}"
  echo "  ${BOLD}${CYAN}╚══════════════════════════════════════════╝${RESET}"
  echo "  OS: $OS"
  discover_skills
  if [[ ${#SKILLS[@]} -eq 0 ]]; then
    echo "  ${RED}No skills found. Run from repo root.${RESET}"
    exit 1
  fi
  echo "  Found ${#SKILLS[@]} skills"
  pick_skills

  local any_sel=0
  local i
  for ((i=0; i<${#SKILL_SEL[@]}; i++)); do
    [[ ${SKILL_SEL[$i]} -eq 1 ]] && { any_sel=1; break; }
  done
  if [[ $any_sel -eq 0 ]]; then
    echo "  ${YELLOW}No skills selected. Exiting.${RESET}"
    exit 0
  fi

  pick_tools
  pick_scope
  run_install "$INSTALL_SCOPE"
  print_summary

  echo "  ${BOLD}Done!${RESET} Skills are ready for your AI coding tools."
  echo
}

main "$@"
