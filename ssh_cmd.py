#!/usr/bin/env python3
"""
SSH command executor for claude-ssh plugin.
Usage: python ssh_cmd.py "<command>"

Reads connection config from config.json in the same directory.
Connects via SSH key (primary) or password (fallback), executes the command,
prints stdout/stderr, and exits with the remote exit code.
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(
            "ERROR: No config.json found in plugin directory.\n"
            "Run the ssh skill setup flow to configure your connection.",
            file=sys.stderr,
        )
        sys.exit(2)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    required = ["hostname", "username"]
    for key in required:
        if not config.get(key):
            print(f"ERROR: '{key}' is missing in config.json.", file=sys.stderr)
            sys.exit(2)

    if not config.get("key_file") and not config.get("password"):
        print(
            "ERROR: Either 'key_file' or 'password' must be set in config.json.",
            file=sys.stderr,
        )
        sys.exit(2)

    return config


def main():
    if len(sys.argv) < 2:
        print("Usage: python ssh_cmd.py '<command>'", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    command = " ".join(sys.argv[1:])

    try:
        import paramiko
    except ImportError:
        print(
            "ERROR: paramiko is not installed. Run: pip install paramiko",
            file=sys.stderr,
        )
        sys.exit(2)

    hostname = config["hostname"]
    username = config["username"]
    port = config.get("port", 22)
    key_file = config.get("key_file")
    password = config.get("password")

    # Expand ~ in key_file path
    if key_file:
        key_file = os.path.expanduser(key_file)
        if not os.path.exists(key_file):
            print(f"ERROR: SSH key file not found: {key_file}", file=sys.stderr)
            sys.exit(2)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connect_kwargs = {
            "hostname": hostname,
            "port": port,
            "username": username,
            "timeout": 10,
        }

        if key_file:
            connect_kwargs["key_filename"] = key_file
        if password:
            connect_kwargs["password"] = password

        client.connect(**connect_kwargs)

        stdin, stdout, stderr = client.exec_command(command, timeout=300)
        stdin.close()

        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()

        if out:
            print(out, end="")
        if err:
            print(err, file=sys.stderr, end="")

        sys.exit(exit_code)

    except paramiko.AuthenticationException:
        print("ERROR: SSH authentication failed. Check your credentials.", file=sys.stderr)
        sys.exit(3)
    except paramiko.SSHException as e:
        print(f"ERROR: SSH connection error: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    finally:
        client.close()


if __name__ == "__main__":
    main()
