The access log is available at /app/access.log. Parse it and write a JSON report to /app/report.json with the following fields:

- total_requests: integer count of all requests in the log
- unique_ips: integer count of distinct client IP addresses
- top_path: string path with the most requests
- top_paths: list of the top 5 requested paths, each with path and count
- methods: mapping of HTTP method names to request counts
- status_codes: mapping of HTTP status codes to response counts

The report must accurately reflect the sample log and include the correct counts for requests, client IPs, HTTP methods, and status codes.
