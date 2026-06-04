import re
import os
from datetime import datetime

# --- Expected log line format ---
# 2025-01-03 06:42:11 | ETCH-02 | A003 | Chamber Pressure Out of Range | HIGH | 47min

LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*"
    r"(?P<equipment>[^\|]+)\s*\|\s*"
    r"(?P<code>[^\|]+)\s*\|\s*"
    r"(?P<description>[^\|]+)\s*\|\s*"
    r"(?P<severity>[^\|]+)\s*\|\s*"
    r"(?P<duration>\d+)min"
)

def parse_line(line):
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    return {
        "timestamp": datetime.strptime(match.group("timestamp"), "%Y-%m-%d %H:%M:%S"),
        "equipment": match.group("equipment").strip(),
        "code": match.group("code").strip(),
        "description": match.group("description").strip(),
        "severity": match.group("severity").strip(),
        "duration_min": int(match.group("duration")),
    }

def parse_log(input_path="data/raw/alarm_log.txt"):
    if not os.path.exists(input_path):
        print(f"Log file not found: {input_path}")
        return []

    records = []
    skipped = 0

    with open(input_path, "r") as f:
        for line in f:
            if line.strip() == "":
                continue
            result = parse_line(line)
            if result:
                records.append(result)
            else:
                skipped += 1

    print(f"Parsed {len(records)} records. Skipped {skipped} unreadable lines.")
    return records

if __name__ == "__main__":
    records = parse_log()
    # Preview first 3 records
    for r in records[:3]:
        print(r)