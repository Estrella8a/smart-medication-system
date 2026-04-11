import sqlite3
from database import connect_db

def get_missed_doses_by_hour():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT time, status
            FROM dose_logs
        """)

        data = cursor.fetchall()
        conn.close()

        hour_stats = {}

        for time, status in data:

            if not time:
                continue

            hour = time[:2]

            if hour not in hour_stats:
                hour_stats[hour] = {"missed": 0, "total": 0}

            hour_stats[hour]["total"] += 1

            if status != "taken":
                hour_stats[hour]["missed"] += 1

        return hour_stats

    except Exception as e:
        print("❌ AI ERROR:", e)
        return {}

def get_risky_hours(threshold=0.4):
    stats = get_missed_doses_by_hour()

    risky = []

    for hour, data in stats.items():
        if data["total"] == 0:
            continue

        ratio = data["missed"] / data["total"]

        if ratio >= threshold:
            risky.append(hour)

    return risky

def get_nurse_performance():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nurse_id, status
        FROM dose_logs
        WHERE nurse_id IS NOT NULL
    """)

    data = cursor.fetchall()
    conn.close()

    stats = {}

    for nurse_id, status in data:
        if nurse_id not in stats:
            stats[nurse_id] = {"missed": 0, "total": 0}

        stats[nurse_id]["total"] += 1

        if status != "taken":
            stats[nurse_id]["missed"] += 1

    return stats

def get_worst_nurse():
    stats = get_nurse_performance()

    worst = None
    worst_ratio = 0

    for nurse_id, data in stats.items():
        if data["total"] == 0:
            continue

        ratio = data["missed"] / data["total"]

        if ratio > worst_ratio:
            worst_ratio = ratio
            worst = nurse_id

    return worst, worst_ratio