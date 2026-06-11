# Claude Code Safeguard Hook

A lightweight, robust `pre-tool-use` hook for Claude Code that prevents the execution of destructive bash and SQL commands. 

This hook automatically intercepts:
- `rm -rf`
- `DROP TABLE`
- `git push --force` (and `-f`)
- `TRUNCATE`
- `DELETE FROM` (without a `WHERE` clause)

If Claude attempts to use any of these, the action is blocked, logged to `~/.claude/hooks/blocked.log`, and Claude is immediately notified with an explanation so it can alter its approach safely.

## Installation (1 command!)

Run the following command to download, install, and enable the hook for Claude Code:

```bash
mkdir -p ~/.claude/hooks && curl -sL https://raw.githubusercontent.com/claude-builders-bounty/claude-builders-bounty/main/safe-bash-hook/pre-tool-use.py -o ~/.claude/hooks/pre-tool-use && chmod +x ~/.claude/hooks/pre-tool-use
```

## How it Works

Claude Code passes tool invocations to any executable named `pre-tool-use` in the `~/.claude/hooks/` directory. This script parses the JSON payload from `stdin` to analyze the `Bash` command payload.

If a destructive pattern is found:
1. It logs the timestamp, exact command, and project directory to `~/.claude/hooks/blocked.log`.
2. It prints an error message explicitly telling Claude to rethink its approach.
3. It exits with code `1`, causing Claude Code to block execution and feed the error message back to the LLM.
4. If the command is completely safe, it exits with code `0`, and Claude Code proceeds seamlessly!
