# claude-ssh

A Claude Code plugin that lets you execute commands on remote servers via SSH.

## Installation

### Local testing

```bash
claude --plugin-dir /path/to/claude-ssh
```

### From GitHub

```bash
# Step 1: Add the marketplace
/plugin marketplace add fabiopauli/claude-ssh

# Step 2: Install the plugin
/plugin install claude-ssh@fabiopauli-claude-ssh
```

## Setup

On first use, the plugin will interactively ask you for:

1. **Hostname** - your server's IP or domain
2. **Username** - SSH login user (e.g., `root`)
3. **Port** - SSH port (default: 22)
4. **SSH key path** - path to your private key (preferred auth method)
5. **Password** - fallback if no SSH key is available

The config is saved locally in `config.json` (gitignored) and reused for future sessions.

## Usage

### Via skill invocation

```
/claude-ssh:ssh uptime
/claude-ssh:ssh df -h
/claude-ssh:ssh systemctl status nginx
```

### Natural language

Just ask Claude to run commands on your server:

```
"Check my server's disk usage"
"Restart the nginx service"
"Show the last 50 lines of /var/log/syslog"
```

## Authentication

The plugin prioritizes auth methods in this order:

1. **SSH private key** (recommended) - provide the path to your key file (e.g., `~/.ssh/id_ed25519`)
2. **Password** - used only if no key is configured

## Requirements

- Python 3.8+
- `paramiko` (installed automatically on first use)

## Security

- `config.json` is gitignored and never committed
- SSH keys are referenced by path, not copied into the plugin
- The plugin uses `paramiko.AutoAddPolicy()` for host key verification

## License

MIT
