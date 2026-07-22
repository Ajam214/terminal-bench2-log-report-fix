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
    valid_lines = 0
    
    # Apache log format pattern
    log_pattern = r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+(?P<status>\d+)\s+(?P<size>\S+)'
    
    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            total += 1
            
            # Extract IP
            try:
                ip = line.split()[0]
                ips.add(ip)
            except IndexError:
                continue
            
            # Parse with regex for detailed info
            match = re.search(log_pattern, line)
            if match:
                valid_lines += 1
                path = match.group('path')
                method = match.group('method')
                status = match.group('status')
                
                paths[path] += 1
                methods[method] += 1
                status_codes[status] += 1
    
    if total == 0:
        raise ValueError("Access log is empty")
    
    # Build report
    report = {
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
    
    return report

def main():
    try:
        log_file = "/app/access.log"
        output_file = "/app/report.json"
        
        report = parse_access_log(log_file)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to {output_file}")
        print(f"Total requests: {report['total_requests']}")
        print(f"Unique IPs: {report['unique_ips']}")
        print(f"Top path: {report['top_path']}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
