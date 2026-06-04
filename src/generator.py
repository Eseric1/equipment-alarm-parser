import random
import os
from datetime import datetime, timedelta

# --- Configuration ---
EQUIPMENT_IDS = ["ETCH-01", "ETCH-02", "ETCH-03", "CVD-01", "CMP-01"]
ALARM_CODES = {
    "A001": "RF Power Fault",
    "A002": "Gas Flow Deviation",
    "A003": "Chamber Pressure Out of Range",
    "A004": "Temperature Exceedance",
    "A005": "End Point Detection Failure",
    "A006": "Wafer Transfer Error",
    "A007": "Pump Speed Low",
    "A008": "Coolant Flow Fault",
}
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

def generate_log(num_entries=200, output_path="data/raw/alarm_log.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    start_time = datetime.now() - timedelta(days=30)

    with open(output_path, "w") as f:
        for _ in range(num_entries):
            # Advance time by a random interval
            start_time += timedelta(minutes=random.randint(1, 240))

            equipment = random.choice(EQUIPMENT_IDS)
            code = random.choice(list(ALARM_CODES.keys()))
            description = ALARM_CODES[code]
            severity = random.choices(
                SEVERITIES, weights=[40, 30, 20, 10]
            )[0]
            duration = random.randint(1, 120)

            line = (
                f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{equipment} | {code} | {description} | "
                f"{severity} | {duration}min\n"
            )
            f.write(line)

    print(f"Log generated: {output_path} ({num_entries} entries)")

if __name__ == "__main__":
    generate_log()