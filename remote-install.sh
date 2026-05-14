#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# skills Remote Installer
# Install agent skills from anywhere with a single command:
#   curl -sSL https://raw.githubusercontent.com/hongphuc5497/skills/main/remote-install.sh | bash
#
# Non-interactive mode (skip menus):
#   curl -sSL ... | bash -s -- --skills "code-review,auto-push" --tools "Claude Code" --scope global
#   curl -sSL ... | bash -s -- --all --tools "Claude Code,Cursor" --scope project
# ============================================================================

REPO_OWNER="hongphuc5497"
REPO_NAME="skills"
DEFAULT_BRANCH="main"
TARBALL_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}/archive/refs/heads/${DEFAULT_BRANCH}.tar.gz"

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
TMPDIR=""
OS=""
SKILLS=()
SKILL_DESCS=()
SKILL_SEL=()
TOOLS=("Claude Code" "Cursor" "Windsurf" "GitHub Copilot" "OpenAI Codex" "OpenCode")
TOOL_SEL=()
INSTALL_SCOPE=""
INSTALLED=()
INSTALL_ALL_TOOLS=0
INSTALL_ALL_SKILLS=0
MODE=""  # "interactive" or "noninteractive"

# ─── Parse flags ────────────────────────────────────────────────────────────
parse_args() {
  MODE="interactive"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --skills) shift; IFS=',' read -ra names <<< "$1"; MODE="noninteractive"
        local i
        for ((i=0; i<${#SKILLS[@]}; i++)); do
          local name="${SKILLS[$i]}"
          local match=0
          local n
          for n in "${names[@]}"; do
            [[ "$name" == "$n" ]] && { match=1; break; }
          done
          [[ $match -eq 1 ]] && SKILL_SEL[$i]=1 || SKILL_SEL[$i]=0
        done ;;
      --tools) shift; IFS=',' read -ra tnames <<< "$1"; MODE="noninteractive"
        local i
        for ((i=0; i<${#TOOLS[@]}; i++)); do
          local tool="${TOOLS[$i]}"
          local match=0
          local t
          for t in "${tnames[@]}"; do
            [[ "$tool" == "$t" ]] && { match=1; break; }
          done
          [[ $match -eq 1 ]] && TOOL_SEL[$i]=1 || TOOL_SEL[$i]=0
        done ;;
      --scope) shift; INSTALL_SCOPE="$1"; MODE="noninteractive" ;;
      --all) INSTALL_ALL_SKILLS=1; MODE="noninteractive" ;;
    esac
    shift
  done
  if [[ $INSTALL_ALL_SKILLS -eq 1 ]]; then
    local i
    for ((i=0; i<${#SKILL_SEL[@]}; i++)); do SKILL_SEL[$i]=1; done
  fi
}

# ─── OS detection ───────────────────────────────────────────────────────────
detect_os() {
  case "$(uname -s)" in
    Darwin*)  OS="macOS" ;;
    Linux*)   OS="Linux" ;;
    CYGWIN*|MINGW*|MSYS*) OS="Windows" ;;
    *) OS="Unknown" ;;
  esac
}

# ─── Discover skills from tarball ──────────────────────────────────────────
discover_skills() {
  local dir desc prev_nullglob
  prev_nullglob=$(shopt -p nullglob)
  shopt -s nullglob
  for dir in "$TMPDIR"/skills/ "$TMPDIR"/*/skills/; do
    [[ -d "$dir" ]] || continue
    local skill_dir
    for skill_dir in "$dir"*/ "$dir"*/*/; do
      [[ -f "$skill_dir/SKILL.md" ]] || continue
      local name
      name="$(basename "$skill_dir")"
      desc=$(awk '/^---$/{n++; next} n==1 && /^description:/{sub(/^description: *"?/, ""); sub(/"$/, ""); print; exit}' "$skill_dir/SKILL.md")
      if [[ ${#desc} -gt 70 ]]; then
        desc="${desc:0:67}..."
      fi
      SKILLS+=("$name")
      SKILL_DESCS+=("$desc")
      SKILL_SEL+=(0)
    done
    break
  done
  eval "$prev_nullglob"
}

# ─── Tool paths ──────────────────────────────────────────────────────────────
get_tool_paths() {
  local tool="$1" scope="$2"
  case "$tool" in
    "Claude Code")
      [[ "$scope" == "project" ]] && echo ".claude/skills" || echo "$HOME/.claude/skills" ;;
    "Cursor")
      [[ "$scope" == "project" ]] && echo ".cursor/rules" || echo "$HOME/.agents/skills" ;;
    "Windsurf")
      [[ "$scope" == "project" ]] && echo ".windsurf/rules" || echo "$HOME/.agents/skills" ;;
    "GitHub Copilot")
      [[ "$scope" == "project" ]] && echo ".github/instructions" || echo "$HOME/.agents/skills" ;;
    "OpenAI Codex")
      [[ "$scope" == "project" ]] && echo ".codex/skills" || echo "$HOME/.codex/skills" ;;
    "OpenCode")
      [[ "$scope" == "project" ]] && echo ".opencode/skills" || echo "$HOME/.agents/skills" ;;
    *)
      [[ "$scope" == "project" ]] && echo ".agents/skills" || echo "$HOME/.agents/skills" ;;
  esac
}

# ─── TUI: scope ─────────────────────────────────────────────────────────────
pick_scope() {
  echo
  echo "  ${BOLD}Install scope?${RESET}"
  echo "    ${BOLD}1${RESET}) Global  — ~/.agents/skills/ etc. (all projects)"
  echo "    ${BOLD}2${RESET}) Project — install to local directory"
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

# ─── TUI: skills ────────────────────────────────────────────────────────────
pick_skills() {
  local idx=0 key
  tput civis 2>/dev/null || true
  while true; do
    echo -ne "\033[H\033[J" 2>/dev/null || clear
    echo "  ${BOLD}Select skills to install${RESET} (↑↓ navigate, Space toggle, Enter done)"
    echo
    printf "  %-4s %-30s %s\n" "" "SKILL" "DESCRIPTION"
    local i
    for ((i=0; i<${#SKILLS[@]}; i++)); do
      if [[ $i -eq $idx ]]; then
        [[ ${SKILL_SEL[$i]} -eq 1 ]] && mark="${GREEN}▶ [✓]" || mark="${CYAN}▶ [ ]"
        printf "  ${mark}${RESET} %-30s %s\n" "${SKILLS[$i]}" "${SKILL_DESCS[$i]}"
      else
        [[ ${SKILL_SEL[$i]} -eq 1 ]] && mark="${GREEN}  [✓]" || mark="${DIM}  [ ]"
        printf "  ${mark}${RESET} %-30s %s\n" "${SKILLS[$i]}" "${SKILL_DESCS[$i]}"
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

# ─── TUI: tools ─────────────────────────────────────────────────────────────
pick_tools() {
  local idx=0 key
  tput civis 2>/dev/null || true
  while true; do
    echo -ne "\033[H\033[J" 2>/dev/null || clear
    echo "  ${BOLD}Select target tools${RESET} (↑↓ navigate, Space toggle, Enter done)"
    echo "  ${DIM}Install All${RESET} toggles every tool at once"
    echo
    if [[ $idx -eq 0 ]]; then
      [[ $INSTALL_ALL_TOOLS -eq 1 ]] && mark="${GREEN}▶ [✓]" || mark="${CYAN}▶ [ ]"
      echo "  ${mark}${RESET} Install All"
    else
      [[ $INSTALL_ALL_TOOLS -eq 1 ]] && mark="${GREEN}  [✓]" || mark="${DIM}  [ ]"
      echo "  ${mark}${RESET} Install All"
    fi
    local i
    for ((i=0; i<${#TOOLS[@]}; i++)); do
      local display_idx=$((i + 1))
      if [[ $display_idx -eq $idx ]]; then
        [[ ${TOOL_SEL[$i]} -eq 1 ]] && mark="${GREEN}▶ [✓]" || mark="${CYAN}▶ [ ]"
        printf "  ${mark}${RESET} %s\n" "${TOOLS[$i]}"
      else
        [[ ${TOOL_SEL[$i]} -eq 1 ]] && mark="${GREEN}  [✓]" || mark="${DIM}  [ ]"
        printf "  ${mark}${RESET} %s\n" "${TOOLS[$i]}"
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
        TOOL_SEL[$((idx - 1))]=$(( 1 - TOOL_SEL[$((idx - 1))] ))
      fi
    elif [[ $key == "" || $key == $'\n' ]]; then
      break
    fi
  done
  tput cnorm 2>/dev/null || true
}

# ─── Install one skill ──────────────────────────────────────────────────────
install_skill() {
  local skill="$1" tool="$2" dest_base="$3" src="$4"
  local dest="$dest_base/$skill"
  if [[ -d "$dest" ]]; then
    echo "  ${YELLOW}⚠${RESET} $skill already at $dest (skip)"
    return
  fi
  mkdir -p "$dest"
  local item
  for item in "$src"/* "$src"/.*; do
    [[ -e "$item" ]] || continue
    local base
    base="$(basename "$item")"
    [[ "$base" == "." || "$base" == ".." ]] && continue
    if [[ -d "$item" && -f "$item/SKILL.md" ]]; then
      continue
    fi
    cp -r "$item" "$dest/" 2>/dev/null || true
  done
  INSTALLED+=("$skill → $tool → $dest")
  echo "  ${GREEN}✓${RESET} $skill → $dest"
}

# ─── Run install ────────────────────────────────────────────────────────────
run_install() {
  local scope="$1" sel_idx=0
  local dest_base
  for ((sel_idx=0; sel_idx<${#SKILLS[@]}; sel_idx++)); do
    [[ ${SKILL_SEL[$sel_idx]} -eq 1 ]] || continue
    local skill="${SKILLS[$sel_idx]}"
    local src
    # Find the skill dir in tarball
    src=$(find "$TMPDIR" -type d -name "$skill" -exec test -f '{}/SKILL.md' \; -print 2>/dev/null | head -1)
    [[ -z "$src" ]] && { echo "  ${YELLOW}⚠${RESET} Source for $skill not found (skip)"; continue; }
    if [[ $INSTALL_ALL_TOOLS -eq 1 ]]; then
      local t
      for t in "${TOOLS[@]}"; do
        dest_base=$(get_tool_paths "$t" "$scope")
        install_skill "$skill" "$t" "$dest_base" "$src"
      done
    else
      local ti
      for ((ti=0; ti<${#TOOLS[@]}; ti++)); do
        [[ ${TOOL_SEL[$ti]} -eq 1 ]] || continue
        dest_base=$(get_tool_paths "${TOOLS[$ti]}" "$scope")
        install_skill "$skill" "${TOOLS[$ti]}" "$dest_base" "$src"
      done
    fi
  done
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

# ─── Cleanup ────────────────────────────────────────────────────────────────
cleanup_tmp() {
  [[ -n "$TMPDIR" && -d "$TMPDIR" ]] && rm -rf "$TMPDIR"
}

# ─── Main ───────────────────────────────────────────────────────────────────
main() {
  detect_os
  echo
  echo "  ${BOLD}${CYAN}╔══════════════════════════════════════════╗${RESET}"
  echo "  ${BOLD}${CYAN}║   Agent Skills Remote Installer          ║${RESET}"
  echo "  ${BOLD}${CYAN}╚══════════════════════════════════════════╝${RESET}"
  echo "  OS: $OS"

  # Download tarball
  TMPDIR=$(mktemp -d)
  trap cleanup_tmp EXIT
  echo "  Downloading ${REPO_OWNER}/${REPO_NAME}..."
  if command -v curl &>/dev/null; then
    curl -sL "$TARBALL_URL" | tar xz -C "$TMPDIR" 2>/dev/null
  elif command -v wget &>/dev/null; then
    wget -qO- "$TARBALL_URL" | tar xz -C "$TMPDIR" 2>/dev/null
  else
    echo "  ${RED}Need curl or wget${RESET}"
    exit 1
  fi
  echo "  Done."

  discover_skills
  if [[ ${#SKILLS[@]} -eq 0 ]]; then
    echo "  ${RED}No skills found.${RESET}"
    exit 1
  fi
  echo "  Found ${#SKILLS[@]} skills"

  parse_args "$@"

  if [[ "$MODE" == "interactive" ]]; then
    pick_skills
    local any_sel=0 i
    for ((i=0; i<${#SKILL_SEL[@]}; i++)); do
      [[ ${SKILL_SEL[$i]} -eq 1 ]] && { any_sel=1; break; }
    done
    if [[ $any_sel -eq 0 ]]; then
      echo "  ${YELLOW}No skills selected. Exiting.${RESET}"
      exit 0
    fi
    pick_tools
    pick_scope
  fi

  if [[ -z "$INSTALL_SCOPE" ]]; then
    INSTALL_SCOPE="global"
  fi

  run_install "$INSTALL_SCOPE"
  print_summary

  echo "  ${BOLD}Done!${RESET} Skills are ready for your AI coding tools."
  echo
}

main "$@"
