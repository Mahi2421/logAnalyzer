# Server Health Bot Lab

Docker-based lab with three SSH servers: web-01 (2221), db-01 (2222), app-01 (2223).

## Setup
Activate the virtual environment with `source .venv/bin/activate` and install dependencies using `pip install -r requirements.txt`.

## Start servers
`docker compose up -d`

## Remote health checks
`python3 remote_check.py web-01`
`python3 remote_check.py --all`

## Local health report
`python3 health.py`

## Port checker
`python3 portcheck.py 127.0.0.1 2221 2222 2223 9999`

## TCP echo test
Start the server: `python3 echo_server.py --port 5001`
In another terminal: `python3 echo_client.py "Hello from the TCP client" --host 127.0.0.1 --port 5001`

## Security and notes
Keep SSH private keys and secrets out of version control. Configure SSH_KEY_PATH in .env. Container memory reported by /proc/meminfo may reflect host memory.
