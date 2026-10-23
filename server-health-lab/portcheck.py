
#!/usr/bin/env python3

import argparse
import socket


def check_port(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "open"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "closed"


def main():
    parser = argparse.ArgumentParser(
        description="Check whether TCP ports are open or closed."
    )
    parser.add_argument("host", help="Hostname or IP address")
    parser.add_argument(
        "ports",
        nargs="+",
        type=int,
        help="One or more TCP ports to check",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Connection timeout in seconds (default: 1.0)",
    )

    args = parser.parse_args()

    if not 0 <= args.timeout:
        parser.error("timeout must be non-negative")

    for port in args.ports:
        if not 1 <= port <= 65535:
            parser.error(f"invalid port: {port}; use 1–65535")

    for port in args.ports:
        status = check_port(args.host, port, args.timeout)
        print(f"{args.host}:{port} - {status}")


if __name__ == "__main__":
    main()
