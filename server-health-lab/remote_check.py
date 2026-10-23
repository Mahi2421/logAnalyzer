
import argparse
import json
import os
import sys
import tempfile

import paramiko
from dotenv import load_dotenv

SERVERS = {
    "web-01": ("127.0.0.1", 2221),
    "db-01": ("127.0.0.1", 2222),
    "app-01": ("127.0.0.1", 2223),
}

USERNAME = "ops"
REMOTE_SCRIPT = "/tmp/health.py"


def check_server(name, host, port, key_path):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        client.connect(
            hostname=host,
            port=port,
            username=USERNAME,
            key_filename=key_path,
            timeout=5,
            banner_timeout=5,
            auth_timeout=5,
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as script:
            script.write(
                open("health.py", encoding="utf-8").read()
            )
            local_script = script.name

        try:
            sftp = client.open_sftp()
            try:
                sftp.put(local_script, REMOTE_SCRIPT)
            finally:
                sftp.close()
        finally:
            os.unlink(local_script)

        stdin, stdout, stderr = client.exec_command(
            "python3 /tmp/health.py",
            timeout=15,
        )

        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        exit_code = stdout.channel.recv_exit_status()

        if exit_code != 0:
            raise RuntimeError(error or f"Remote exit code: {exit_code}")

        report = json.loads(output)

        return {
            "server": name,
            "status": "success",
            "health": report,
        }

    except Exception as exc:
        return {
            "server": name,
            "status": "failed",
            "error": str(exc),
        }

    finally:
        client.close()


def main():
    load_dotenv()

    key_path = os.getenv("SSH_KEY_PATH")
    if not key_path or not os.path.isfile(key_path):
        print("Error: SSH_KEY_PATH is missing or the key file does not exist.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Collect health reports from remote lab servers."
    )
    parser.add_argument(
        "server",
        nargs="?",
        choices=SERVERS.keys(),
        help="Name of the server to check",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Check all configured servers",
    )
    args = parser.parse_args()

    if not args.all and not args.server:
        parser.error("Specify a server name or use --all.")

    targets = SERVERS if args.all else {args.server: SERVERS[args.server]}

    results = [
        check_server(name, host, port, key_path)
        for name, (host, port) in targets.items()
    ]

    print(json.dumps(results, indent=2))

    if any(result["status"] == "failed" for result in results):
        sys.exit(1)


if __name__ == "__main__":
    main()

