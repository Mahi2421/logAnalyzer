#!/bin/sh
set -eu

echo "===== SERVER HEALTH REPORT ====="

echo "Hostname:"
hostname

echo "Current date:"
date

echo "System uptime:"
uptime

echo "Disk space:"
df -h

echo "Memory:"
free -h

echo "IP addresses:"
hostname -I || true

echo "Health report completed."
