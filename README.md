# Log Report Parser

## Overview
Parse Apache access logs and generate a JSON report with traffic statistics.

## What it does
- Reads `/app/access.log` (Apache-style access log)
- Counts total requests and unique IPs
- Identifies the most popular page
- Outputs results to `/app/report.json`

## Files
- `solution/solve.py` - Main script that generates the report
- `solution/solve_improved.py` - Enhanced version with better error handling
- `tests/test_outputs.py` - Basic tests
- `tests/test_comprehensive.py` - Extended tests

## Running it
```
python solve.py
```

This will read the access log and create a JSON report with:
- total_requests
- unique_ips  
- top_path
- top_paths (list of top 5)
- methods (GET, POST counts)
- status_codes (200, 401, etc)

## Log format
Standard Apache access log format:
```
192.168.0.1 - - [16/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
```

## Tests
Run tests with:
```
pytest tests/ -v
```

Currently passing 17 tests covering file existence, data correctness, and edge cases.
