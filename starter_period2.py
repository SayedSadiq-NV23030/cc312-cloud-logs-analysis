"""
PL202 - Day 1 (Period 2) Starter File
Task: Cloud Log Cleaner + JSON Summary (Mini Project)

You will:
1) Read logs.txt
2) Keep ONLY valid lines (4 parts AND level is INFO/WARN/ERROR)
3) Write clean logs to clean_logs.txt (same original format)
4) Create summary.json with:
   - total_lines, valid_lines, invalid_lines
   - levels: counts of INFO/WARN/ERROR (valid only)
   - top_services: top 3 services by valid log count
   - top_errors: top 3 ERROR messages by count (valid ERROR only)

IMPORTANT:
- Work independently (no teacher / classmates).
- You may copy your solutions from Period 1.
"""

import json
from pathlib import Path
from collections import Counter

LOG_FILE = Path("logs.txt")
CLEAN_FILE = Path("clean_logs.txt")
SUMMARY_FILE = Path("summary.json")

ALLOWED_LEVELS = {"INFO", "WARN", "ERROR"}


def parse_line(line: str):
    """
    Returns (timestamp, level, service, message) OR None if format invalid.
    """
    # TODO 1: Implement parse_line (same rules as Period 1)
    line = line.strip()
    if not line:
        return None
    parts = [p.strip() for p in line.split('|')]
    if len(parts) != 4:
        return None
    return tuple(parts)


def normalize_level(level: str) -> str:
    # TODO 2: return uppercase level
    return level.upper()


def main():
    if not LOG_FILE.exists():
        print(f"ERROR: Could not find {LOG_FILE}. Make sure logs.txt is in the same folder.")
        return

    total_lines = 0
    valid_lines = 0
    invalid_lines = 0

    level_counts = {"INFO": 0, "WARN": 0, "ERROR": 0}

    service_counter = Counter()
    error_message_counter = Counter()

    clean_lines = []  # store valid lines to write later

    # TODO 3: Read logs.txt line by line
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            parsed = parse_line(line)
            if parsed is None:
                invalid_lines += 1
                continue
            timestamp, level, service, message = parsed
            norm_level = normalize_level(level)
            if norm_level not in ALLOWED_LEVELS:
                invalid_lines += 1
                continue
            # Valid line
            valid_lines += 1
            level_counts[norm_level] += 1
            service_counter[service] += 1
            if norm_level == "ERROR":
                error_message_counter[message] += 1
            # Cleaned-format line
            clean_lines.append(f"{timestamp} | {norm_level} | {service} | {message}")

    # TODO 4: Write clean_lines into clean_logs.txt (one per line)
    with CLEAN_FILE.open("w", encoding="utf-8") as out:
        for cl in clean_lines:
            out.write(cl + "\n")

    # TODO 5: Build the summary dictionary with this exact structure:
    summary = {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "invalid_lines": invalid_lines,
        "levels": dict(level_counts),
        "top_services": [
            {"service": svc, "count": cnt}
            for svc, cnt in service_counter.most_common(3)
        ],
        "top_errors": [
            {"message": msg, "count": cnt}
            for msg, cnt in error_message_counter.most_common(3)
        ],
    }

    # TODO 6: Save summary.json using json.dump(..., indent=2)
    with SUMMARY_FILE.open("w", encoding="utf-8") as out:
        json.dump(summary, out, indent=2)

    # Optional self-check prints (you can keep them):
    print("Valid:", valid_lines, "Invalid:", invalid_lines)


if __name__ == "__main__":
    main()
