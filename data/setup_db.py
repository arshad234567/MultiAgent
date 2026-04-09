
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "market_risk.db")


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()


    c.executescript("""
        CREATE TABLE IF NOT EXISTS desk_hierarchy (
            desk_id       TEXT PRIMARY KEY,
            desk_name     TEXT,
            portfolio     TEXT,
            trader_id     TEXT,
            business_line TEXT
        );

        CREATE TABLE IF NOT EXISTS breach_groups (
            breach_group_id INTEGER PRIMARY KEY,
            situation_id    INTEGER,
            measure_id      INTEGER,
            business_date   TEXT,
            actual_value    REAL,
            limit_value     REAL,
            threshold_type  TEXT,
            governing_body  TEXT,
            desk_id         TEXT,
            FOREIGN KEY (desk_id) REFERENCES desk_hierarchy(desk_id)
        );

        CREATE TABLE IF NOT EXISTS response_plans (
            breach_group_id  INTEGER PRIMARY KEY,
            response_plan_url TEXT,
            jira_ticket       TEXT,
            FOREIGN KEY (breach_group_id) REFERENCES breach_groups(breach_group_id)
        );

        CREATE TABLE IF NOT EXISTS breach_history (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            breach_group_id     INTEGER,
            desk_id             TEXT,
            measure_id          INTEGER,
            business_date       TEXT,
            actual_value        REAL,
            limit_value         REAL,
            severity_assigned   TEXT,
            resolution_days     INTEGER,
            root_cause_category TEXT
        );
    """)

    desks = [
        ("DESK-EQ-01", "Equity Derivatives Desk",  "EU Equity Book",    "T-001", "Equities"),
        ("DESK-FI-01", "Fixed Income Trading Desk", "EM Rates Book",     "T-002", "Fixed Income"),
        ("DESK-CR-01", "Credit Trading Desk",       "HY Credit Book",    "T-003", "Credit"),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO desk_hierarchy VALUES (?,?,?,?,?)", desks
    )

    breaches = [
        # CRITICAL: 34% over VaR limit
        (557417, 302, 646537, "2024-02-10", 1340000.0, 1000000.0, "VaR",         "Group Risk Committee", "DESK-EQ-01"),
        # HIGH:     15% over Stress Loss limit
        (557420, 305, 646540, "2024-02-11",  575000.0,  500000.0, "Stress Loss", "Market Risk Committee","DESK-FI-01"),
        # MEDIUM:   8% over Sensitivity limit
        (557431, 310, 646550, "2024-02-12",   54000.0,   50000.0, "Sensitivity", "Desk Risk Committee",  "DESK-CR-01"),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO breach_groups VALUES (?,?,?,?,?,?,?,?,?)", breaches
    )


    plans = [
        (557417, "https://confluence.firm.com/rp/557417", "RISK-1042"),
        (557420, "https://confluence.firm.com/rp/557420", "RISK-1043"),
        (557431, None, None),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO response_plans VALUES (?,?,?)", plans
    )


    history = [
        # DESK-EQ-01 VaR history — recurring breaches → CRITICAL
        (557400, "DESK-EQ-01", 646537, "2024-01-28", 1280000.0, 1000000.0, "CRITICAL", 3, "Delta spike"),
        (557380, "DESK-EQ-01", 646537, "2024-01-15", 1210000.0, 1000000.0, "HIGH",     2, "Vol regime shift"),
        (557360, "DESK-EQ-01", 646537, "2024-01-03", 1180000.0, 1000000.0, "HIGH",     2, "Position buildup"),
        (557340, "DESK-EQ-01", 646537, "2023-12-18",  980000.0, 1000000.0, "MEDIUM",   1, "End of day"),
        (557320, "DESK-EQ-01", 646537, "2023-11-30", 1150000.0, 1000000.0, "HIGH",     4, "Market stress"),
        # DESK-FI-01 Stress Loss history — occasional
        (557390, "DESK-FI-01", 646540, "2024-01-20",  530000.0,  500000.0, "HIGH",     3, "Rate shock"),
        (557370, "DESK-FI-01", 646540, "2023-12-05",  510000.0,  500000.0, "MEDIUM",   1, "Duration drift"),
        # DESK-CR-01 Sensitivity — first time
    ]
    c.executemany(
        "INSERT OR IGNORE INTO breach_history "
        "(breach_group_id,desk_id,measure_id,business_date,actual_value,"
        "limit_value,severity_assigned,resolution_days,root_cause_category) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        history
    )

    conn.commit()
    conn.close()
    print(f"[DB] Database ready at: {DB_PATH}")


if __name__ == "__main__":
    setup_database()
