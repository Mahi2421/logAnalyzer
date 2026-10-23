
#!/usr/bin/env python3

import json
import shutil
import socket
from pathlib import Path


def get_uptime():
    try:
        return float(Path("/proc/uptime").read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


def get_load_average():
    try:
        values = Path("/proc/loadavg").read_text().split()
        return {
            "1_min": float(values[0]),
            "5_min": float(values[1]),
            "15_min": float(values[2]),
        }
    except (OSError, ValueError, IndexError):
        return None


def get_memory():
    try:
        info = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, value = line.split(":", 1)
            info[key] = int(value.strip().split()[0]) * 1024

        total = info["MemTotal"]
        available = info.get("MemAvailable", info.get("MemFree", 0))

        return {
            "total_bytes": total,
            "used_bytes": total - available,
        }
    except (OSError, ValueError, KeyError, IndexError):
        return None


def get_disk_usage():
    try:
        usage = shutil.disk_usage("/")
        return {
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "used_percent": round(usage.used / usage.total * 100, 2),
        }
    except OSError:
        return None


def main():
    report = {
        "hostname": socket.gethostname(),
        "uptime_seconds": get_uptime(),
        "load_average": get_load_average(),
        "memory": get_memory(),
        "disk_root": get_disk_usage(),
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
