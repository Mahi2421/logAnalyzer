# logAnalyzer

AI-based log analysis, server health checks, and ChatOps for deployment.

## Overview

logAnalyzer aims to simplify server monitoring by combining log analysis, Linux health checks, and chat-based server management. Server-changing actions should require approval before execution.

## Docker Test Lab

The lab runs three Linux containers using Docker Compose.

| Server | OS | SSH Port |
|---|---|---|
| web-01 | Ubuntu 24.04 | 2221 |
| db-01 | Debian 12 | 2222 |
| app-01 | Rocky Linux 9 | 2223 |

Each server has an `ops` user configured for SSH key authentication and passwordless sudo in this local test environment.

## Prerequisites

- WSL2 with Ubuntu
- Docker Desktop with WSL integration
- Docker Compose and an SSH client

## Start the Lab

Run these commands from the directory containing `docker-compose.yml`:

```bash
docker compose up -d --build
docker compose ps
```

## Connect to Servers

```bash
ssh -i ~/.ssh/server-lab-key -p 2221 ops@localhost
ssh -i ~/.ssh/server-lab-key -p 2222 ops@localhost
ssh -i ~/.ssh/server-lab-key -p 2223 ops@localhost
```

## Health Checks

Run inside a connected server:

```bash
hostname
cat /etc/os-release
sudo -n /usr/local/bin/server-info.sh
```

The health-check script reports system uptime, disk usage, memory, and IP address.

## Stop the Lab

```bash
docker compose down
```

## Security

- SSH password authentication is disabled.
- SSH public-key authentication is enabled.
- Private SSH keys must never be committed to GitHub.
- Passwordless sudo is intended only for this isolated test lab.
- Server-changing ChatOps actions should require explicit approval.

## Status

The three-container Docker lab, SSH access, passwordless sudo, and health-check script have been tested. Further log-analysis and ChatOps functionality should be documented as complete when implemented.

## License

See [LICENSE](LICENSE).
