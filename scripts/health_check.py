#!/usr/bin/env python3
"""
InstituteHub Health Check & Uptime Monitoring Utility
=====================================================
Monitors endpoint availability, HTTP status, TLS/SSL certificates,
disk capacity, and Nginx daemon status with institutional CLI output.
"""

import argparse
import json
import logging
import os
import shutil
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("InstituteHub-HealthCheck")


def check_http_status(url: str, timeout: int = 10) -> dict:
    """Checks HTTP/HTTPS endpoint reachability and response latency."""
    result = {
        "reachable": False,
        "status_code": None,
        "response_time_ms": None,
        "error": None,
    }
    
    start_time = time.perf_counter()
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "InstituteHub-HealthMonitor/1.0"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = (time.perf_counter() - start_time) * 1000
            result["reachable"] = True
            result["status_code"] = response.getcode()
            result["response_time_ms"] = round(latency, 2)
    except urllib.error.HTTPError as e:
        latency = (time.perf_counter() - start_time) * 1000
        result["reachable"] = True
        result["status_code"] = e.code
        result["response_time_ms"] = round(latency, 2)
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
        
    return result


def check_ssl_certificate(hostname: str, port: int = 443, timeout: int = 5) -> dict:
    """Validates SSL certificate expiry and cipher negotiation."""
    result = {
        "valid": False,
        "days_remaining": None,
        "issuer": None,
        "expiry_date": None,
        "error": None,
    }

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert.get("notAfter")
                # Format: 'May 15 12:00:00 2027 GMT'
                expiry = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                days_left = (expiry - now).days

                result["valid"] = days_left > 0
                result["days_remaining"] = days_left
                result["expiry_date"] = expiry.strftime("%Y-%m-%d %H:%M:%S UTC")
                
                issuer_dict = dict(x[0] for x in cert.get("issuer", []))
                result["issuer"] = issuer_dict.get("organizationName", "Unknown CA")
    except Exception as e:
        result["error"] = str(e)

    return result


def check_disk_usage(path: str = ".") -> dict:
    """Calculates disk space metrics for the given partition."""
    result = {
        "total_gb": 0.0,
        "used_gb": 0.0,
        "free_gb": 0.0,
        "percent_used": 0.0,
        "status": "HEALTHY",
    }
    try:
        total, used, free = shutil.disk_usage(path)
        result["total_gb"] = round(total / (1024 ** 3), 2)
        result["used_gb"] = round(used / (1024 ** 3), 2)
        result["free_gb"] = round(free / (1024 ** 3), 2)
        pct = round((used / total) * 100, 1)
        result["percent_used"] = pct
        if pct > 90:
            result["status"] = "CRITICAL"
        elif pct > 80:
            result["status"] = "WARNING"
    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)

    return result


def check_nginx_process() -> dict:
    """Checks if Nginx daemon or system process is running."""
    result = {
        "running": False,
        "details": "Nginx process check",
    }
    
    # Check Linux / UNIX or Windows process list
    try:
        if os.name == "nt":
            import subprocess
            out = subprocess.run(["tasklist"], capture_output=True, text=True, check=False)
            if "nginx.exe" in out.stdout.lower():
                result["running"] = True
                result["details"] = "nginx.exe active in tasklist"
            else:
                result["details"] = "Nginx daemon not running on Windows host (Standalone dev mode)"
        else:
            import subprocess
            out = subprocess.run(["pgrep", "nginx"], capture_output=True, text=True, check=False)
            if out.returncode == 0 and out.stdout.strip():
                result["running"] = True
                result["details"] = "Nginx master/worker processes active"
            else:
                # Check systemctl status
                sys_out = subprocess.run(["systemctl", "is-active", "nginx"], capture_output=True, text=True, check=False)
                if sys_out.stdout.strip() == "active":
                    result["running"] = True
                    result["details"] = "Nginx active via systemd"
                else:
                    result["details"] = "Nginx service inactive"
    except Exception as e:
        result["details"] = f"Process check error: {e}"

    return result


def evaluate_overall_health(http_res: dict, ssl_res: dict, disk_res: dict, local_only: bool) -> str:
    """Determines overall system health classification."""
    if disk_res.get("percent_used", 0) > 90:
        return "CRITICAL"

    if not local_only:
        if not http_res.get("reachable") or (http_res.get("status_code") and http_res.get("status_code") >= 500):
            return "CRITICAL"
        if ssl_res.get("days_remaining") is not None and ssl_res.get("days_remaining") < 7:
            return "CRITICAL"

    if disk_res.get("percent_used", 0) > 80:
        return "WARNING"

    return "HEALTHY"


def format_cli_output(data: dict) -> str:
    """Formats health metrics into the standardized institutional status card."""
    lines = [
        "",
        "InstituteHub Health Check",
        "=========================",
        f"Timestamp     : {data['timestamp']}",
    ]

    if not data["local_only"]:
        http_status_str = f"{data['http']['status_code']} ({data['http']['response_time_ms']} ms)" if data['http']['status_code'] else f"FAILED ({data['http']['error']})"
        lines.append(f"Website       : {'UP' if data['http']['reachable'] else 'DOWN'}")
        lines.append(f"HTTP Status   : {http_status_str}")

        if data["ssl"].get("days_remaining") is not None:
            lines.append(f"HTTPS / SSL   : VALID ({data['ssl']['days_remaining']} days left, Issuer: {data['ssl']['issuer']})")
        elif data["ssl"].get("error"):
            lines.append(f"HTTPS / SSL   : ERROR ({data['ssl']['error']})")
        else:
            lines.append("HTTPS / SSL   : N/A")
    else:
        lines.append("Remote Check  : SKIPPED (--local-only mode)")

    lines.append(f"Disk Usage    : {data['disk']['percent_used']}% used ({data['disk']['free_gb']} GB free of {data['disk']['total_gb']} GB)")
    lines.append(f"Nginx Status  : {'RUNNING' if data['nginx']['running'] else 'INACTIVE'} ({data['nginx']['details']})")
    lines.append("")
    lines.append(f"Overall Status: {data['overall_status']}")
    lines.append("=" * 25)
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="InstituteHub Production Health & Uptime Check")
    parser.add_argument("--url", default="https://institutehub.edu", help="URL to probe (default: https://institutehub.edu)")
    parser.add_argument("--disk-path", default=".", help="Filesystem path for disk usage check")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP request timeout in seconds")
    parser.add_argument("--local-only", action="store_true", help="Perform only local system and disk checks")
    parser.add_argument("--json", action="store_true", help="Output raw JSON metrics")

    args = parser.parse_args()

    parsed_url = urllib.parse.urlparse(args.url)
    hostname = parsed_url.hostname or "localhost"

    # 1. Probe HTTP endpoint
    if not args.local_only:
        http_data = check_http_status(args.url, timeout=args.timeout)
        ssl_data = check_ssl_certificate(hostname, timeout=args.timeout) if parsed_url.scheme == "https" else {}
    else:
        http_data = {}
        ssl_data = {}

    # 2. Local Disk & Process checks
    disk_data = check_disk_usage(args.disk_path)
    nginx_data = check_nginx_process()

    overall = evaluate_overall_health(http_data, ssl_data, disk_data, args.local_only)

    report = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "url": args.url,
        "local_only": args.local_only,
        "http": http_data,
        "ssl": ssl_data,
        "disk": disk_data,
        "nginx": nginx_data,
        "overall_status": overall,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_cli_output(report))

    sys.exit(0 if overall in ["HEALTHY", "WARNING"] else 1)


if __name__ == "__main__":
    main()
