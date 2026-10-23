
#!/usr/bin/env python3

import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="TCP echo client")
    parser.add_argument("message", help="Message to send")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    message = args.message.encode("utf-8") + b"\n"

    with socket.create_connection((args.host, args.port), timeout=3) as client:
        client.sendall(message)

        with client.makefile("rb") as reader:
            reply = reader.readline()

    if reply != message:
        raise RuntimeError("Echo reply did not match the sent message")

    print(reply.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
