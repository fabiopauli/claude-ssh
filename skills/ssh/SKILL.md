---
name: ssh
description: >
  Execute shell commands on a remote server via SSH.
  Use when the user asks to run commands, check status, manage services,
  or perform any operation on their remote server/VPS.
allowed-tools: Bash(python:*), Bash(pip install:*)
argument-hint: <shell command>
---

# SSH Remote Command Execution

You execute shell commands on the user's remote server via SSH.

## Plugin directory

The plugin directory is: `${PLUGIN_DIR}`

## First-time setup

Before running any command, check if `${PLUGIN_DIR}/config.json` exists:

```bash
test -f "${PLUGIN_DIR}/config.json" && echo "EXISTS" || echo "MISSING"
```

### If config.json is MISSING — run interactive setup:

1. **Ask the user** for connection details using AskUserQuestion:
   - **Hostname** (e.g., `192.168.1.100` or `my-server.com`)
   - **Username** (e.g., `root`)
   - **Port** (default: `22`)
   - **Path to SSH private key** (e.g., `~/.ssh/id_ed25519`) — this is the **primary** auth method
   - If no key is available, ask for a **password** as fallback

2. **Install paramiko** if not already available:
   ```bash
   python3 -c "import paramiko" 2>/dev/null || pip install paramiko
   ```

3. **Write the config** to `${PLUGIN_DIR}/config.json`:
   ```json
   {
     "hostname": "<hostname>",
     "username": "<username>",
     "port": 22,
     "key_file": "<path to SSH key or null>",
     "password": "<password or null>"
   }
   ```

4. **Test the connection**:
   ```bash
   python3 "${PLUGIN_DIR}/ssh_cmd.py" "echo connected"
   ```
   If it fails, help the user fix the config and retry.

## Command execution

Once config.json exists, execute the user's command:

```bash
python3 "${PLUGIN_DIR}/ssh_cmd.py" "<command>"
```

### Important notes

- The command timeout is **300 seconds**. Warn the user for long-running commands.
- Users can chain commands with `&&` or `;` inside the argument.
- Present stdout output clearly to the user.
- If stderr has content, show it as an error/warning.
- Exit code 2 means a config or setup problem — guide the user through fixing it.
- Exit code 3 means an SSH connection or authentication error.

## Examples

Single command:
```bash
python3 "${PLUGIN_DIR}/ssh_cmd.py" "uptime"
```

Chained commands:
```bash
python3 "${PLUGIN_DIR}/ssh_cmd.py" "cd /var/log && tail -20 syslog"
```

Service management:
```bash
python3 "${PLUGIN_DIR}/ssh_cmd.py" "systemctl status nginx"
```
