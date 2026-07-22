#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter
from pathlib import Path


def parse_access_log(log_file):
    log_path = Path(log_file)
    if not log_path.exists():
        raise FileNotFoundError(f"Access log not found: {log_file}")

    paths = Counter()
    ips = set()
    methods = Counter()
    status_codes = Counter()
    total = 0

    log_pattern = r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+(?P<status>\d+)\s+(?P<size>\S+)'

    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            total += 1
            parts = line.split()
            if parts:
                ips.add(parts[0])

            match = re.search(log_pattern, line)
            if not match:
                continue

            paths[match.group("path")] += 1
            methods[match.group("method")] += 1
            status_codes[match.group("status")] += 1

    if total == 0:
        raise ValueError("Access log is empty")

    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0] if paths else None,
        "top_paths": [
            {"path": path, "count": count}
            for path, count in paths.most_common(5)
        ],
        "methods": dict(methods),
        "status_codes": dict(status_codes),
    }


def main():
    try:
        report = parse_access_log("/app/access.log")
        with open("/app/report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print("Wrote /app/report.json")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
