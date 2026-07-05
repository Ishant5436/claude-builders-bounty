# Claude Code Safe Bash Hook

A `pre-tool-use` hook for Claude Code that intercepts and blocks dangerous commands such as `rm -rf`, `DROP TABLE`, `TRUNCATE`, and unguarded `DELETE FROM` statements. 

When Claude attempts to run a restricted command, this hook automatically blocks the execution, logs the attempt to `~/.claude/hooks/blocked.log`, and provides clear feedback to Claude on why the command failed.

## Installation (2 Steps)

1. Create the hooks directory and copy the script:
   ```bash
   mkdir -p ~/.claude/hooks && cp pre-tool-use ~/.claude/hooks/
   ```

2. Make it executable:
   ```bash
   chmod +x ~/.claude/hooks/pre-tool-use
   ```

## Blocked Patterns
- `rm -rf`
- `DROP TABLE`
- `git push --force` or `git push -f`
- `TRUNCATE`
- `DELETE FROM` (without a `WHERE` clause)
