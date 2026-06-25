# Lean Terminal - shell integration for bash
if [ -n "$__LOT_SHELL_INTEGRATION" ]; then return 0 2>/dev/null || exit 0; fi
__LOT_SHELL_INTEGRATION=1
__lot_prompt_command() {
  local ec="$?"
  printf '\e]133;D;%s\e\\' "$ec"
  printf '\e]133;A\e\\'
}
if [ -n "$PROMPT_COMMAND" ]; then
  PROMPT_COMMAND="__lot_prompt_command;${PROMPT_COMMAND}"
else
  PROMPT_COMMAND="__lot_prompt_command"
fi
PS0='$(__lot_preexec)'
__lot_preexec() { printf '\e]133;B\e\\'; }
printf '\e]133;A\e\\'