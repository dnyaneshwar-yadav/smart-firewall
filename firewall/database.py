import sqlite3
import config


class Database:

    # =====================================
    # Initialize Database
    # =====================================

    def __init__(self):

        self.connection = sqlite3.connect(
            config.DATABASE_PATH,
            check_same_thread=False
        )

        # Better SQLite Performance

        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA foreign_keys=ON")

        self.cursor = self.connection.cursor()

    # =====================================
    # Create Tables
    # =====================================

    def create_tables(self):

        # -------------------------
        # Logs Table
        # -------------------------

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS logs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            source_ip TEXT,

            destination_ip TEXT,

            protocol TEXT,

            action TEXT,

            reason TEXT

        )

        """)

        # -------------------------
        # Rules Table
        # -------------------------

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS rules(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            rule_type TEXT NOT NULL,

            value TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'ACTIVE',

            created_at TEXT NOT NULL

        )

        """)

        # -------------------------
        # Performance Indexes
        # -------------------------

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_logs_action

        ON logs(action)

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_logs_protocol

        ON logs(protocol)

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_logs_source

        ON logs(source_ip)

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_logs_destination

        ON logs(destination_ip)

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_logs_timestamp

        ON logs(timestamp)

        """)

        self.connection.commit()

    # =====================================
    # Dashboard
    # =====================================

    def get_total_packets(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM logs

        """)

        return self.cursor.fetchone()[0]

    def get_allowed_packets(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM logs

        WHERE action='ALLOW'

        """)

        return self.cursor.fetchone()[0]

    def get_blocked_packets(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM logs

        WHERE action='BLOCK'

        """)

        return self.cursor.fetchone()[0]

    def get_recent_logs(self, limit=10):

        self.cursor.execute("""

        SELECT

            id,

            timestamp,

            source_ip,

            destination_ip,

            protocol,

            action,

            reason

        FROM logs

        ORDER BY id DESC

        LIMIT ?

        """, (

            limit,

        ))

        return self.cursor.fetchall()

    def get_total_rules(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM rules

        """)

        return self.cursor.fetchone()[0]

    # =====================================
    # Analytics
    # =====================================

    def get_protocol_counts(self):

        self.cursor.execute("""

        SELECT

            protocol,

            COUNT(*)

        FROM logs

        GROUP BY protocol

        ORDER BY COUNT(*) DESC

        """)

        return self.cursor.fetchall()

    def get_allow_block_stats(self):

        self.cursor.execute("""

        SELECT

            action,

            COUNT(*)

        FROM logs

        GROUP BY action

        ORDER BY COUNT(*) DESC

        """)

        return self.cursor.fetchall()

    # =====================================
    # Total Logs
    # =====================================

    def get_total_logs(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM logs

        """)

        return self.cursor.fetchone()[0]

    # =====================================
    # Close
    # =====================================

    def close(self):

        self.connection.close()
