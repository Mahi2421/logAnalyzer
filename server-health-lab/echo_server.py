
#!/usr/bin/env python3

import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="TCP echo server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.host, args.port))
        server.listen()

        print(f"Echo server listening on {args.host}:{args.port}")

        while True:
            conn, address = server.accept()

            with conn:
                print(f"Connected by {address}")

                with conn.makefile("rb") as reader:
                    message = reader.readline()

                if message:
                    conn.sendall(message)


if __name__ == "__main__":
    main()
