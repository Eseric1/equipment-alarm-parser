import pandas as pd

def build_dataframe(records):
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["week"] = df["timestamp"].dt.isocalendar().week
    df["date"] = df["timestamp"].dt.date
    return df

def fault_frequency(df):
    return (
        df.groupby(["equipment", "code", "description"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

def downtime_by_equipment(df):
    return (
        df.groupby("equipment")["duration_min"]
        .sum()
        .reset_index(name="total_downtime_min")
        .sort_values("total_downtime_min", ascending=False)
    )

def severity_breakdown(df):
    return (
        df.groupby(["equipment", "severity"])
        .size()
        .reset_index(name="count")
        .sort_values(["equipment", "count"], ascending=[True, False])
    )

def weekly_critical_alarms(df):
    critical = df[df["severity"] == "CRITICAL"]
    return (
        critical.groupby("week")
        .size()
        .reset_index(name="critical_count")
        .sort_values("week")
    )

def repeat_offenders(df, threshold=5):
    freq = fault_frequency(df)
    return freq[freq["count"] >= threshold]

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from src.parser import parse_log

    records = parse_log()
    df = build_dataframe(records)

    print("\n--- Top Faults by Frequency ---")
    print(fault_frequency(df).head(10))

    print("\n--- Total Downtime by Equipment ---")
    print(downtime_by_equipment(df))

    print("\n--- Weekly Critical Alarms ---")
    print(weekly_critical_alarms(df))

    print("\n--- Repeat Offenders (5+ occurrences) ---")
    print(repeat_offenders(df))