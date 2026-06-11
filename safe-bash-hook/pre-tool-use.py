#!/usr/bin/env python3
import sys
import json
import os
import re
from datetime import datetime

def block_command(command, reason):
    """Logs the blocked command and exits with a non-zero status."""
    log_dir = os.path.expanduser("~/.claude/hooks")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "blocked.log")
    
    timestamp = datetime.now().isoformat()
    project_path = os.getcwd()
    
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] command=\"{command}\" project=\"{project_path}\"\n")
    
    # Print the error message which will be sent to Claude as the system response
    print(f"🚫 BLOCKING ACTION: The command was intercepted and blocked by the pre-tool-use security hook.")
    print(f"Reason: {reason}")
    print(f"Blocked Command: {command}")
    print(f"\nPlease formulate a safer alternative or ask the user for explicit permission.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        sys.exit(0)
        
    tool_name = sys.argv[1].lower()
    
    # We only care about shell/bash tools
    if tool_name not in ["bash", "run_command", "terminal"]:
        sys.exit(0)
        
    try:
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)
            
        payload = json.loads(input_data)
    except Exception:
        sys.exit(0)
        
    # Depending on the exact tool interface, the command could be in 'command', 'CommandLine', etc.
    command = payload.get("command") or payload.get("CommandLine") or payload.get("script")
    if not command:
        sys.exit(0)
        
    # Check against blocked patterns
    # Using regex for case-insensitivity and to handle multiple spaces
    
    cmd_upper = command.upper()
    
    if re.search(r'rm\s+-rf', command):
        block_command(command, "Contains destructive 'rm -rf' pattern.")
        
    if "DROP TABLE" in cmd_upper:
        block_command(command, "Contains destructive 'DROP TABLE' statement.")
        
    if re.search(r'git\s+push\s+--force', command) or re.search(r'git\s+push\s+-f\b', command):
        block_command(command, "Contains dangerous 'git push --force' pattern.")
        
    if "TRUNCATE" in cmd_upper:
        block_command(command, "Contains destructive 'TRUNCATE' statement.")
        
    if "DELETE FROM" in cmd_upper and "WHERE" not in cmd_upper:
        block_command(command, "Contains 'DELETE FROM' without a safety 'WHERE' clause.")
        
    # If no patterns match, exit cleanly
    sys.exit(0)

if __name__ == "__main__":
    main()
