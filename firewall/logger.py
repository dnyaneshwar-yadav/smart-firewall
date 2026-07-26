from datetime import datetime
import csv
import os

from firewall.database import Database


class Logger:

    # =====================================
    # Initialize Database
    # =====================================

    def __init__(self):

        self.db = Database()

    # =====================================
    # Save Log
    # =====================================

    def log(
        self,
        source_ip,
        destination_ip,
        protocol,
        action,
        reason
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.db.cursor.execute("""
            INSERT INTO logs
            (
                timestamp,
                source_ip,
                destination_ip,
                protocol,
                action,
                reason
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            source_ip,
            destination_ip,
            protocol,
            action,
            reason
        ))

        self.db.connection.commit()

    # =====================================
    # Get Recent Logs
    # =====================================

    def get_logs(self, limit=50):

        self.db.cursor.execute("""
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

        return self.db.cursor.fetchall()

    # =====================================
    # Search Logs
    # =====================================

    def search_logs(self, keyword, limit=50):

        self.db.cursor.execute("""
            SELECT
                id,
                timestamp,
                source_ip,
                destination_ip,
                protocol,
                action,
                reason
            FROM logs
            WHERE
                source_ip LIKE ?
                OR destination_ip LIKE ?
            ORDER BY id DESC
            LIMIT ?
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            limit
        ))

        return self.db.cursor.fetchall()

    # =====================================
    # Filter Logs
    # =====================================

    def filter_logs(self, action, limit=50):

        self.db.cursor.execute("""
            SELECT
                id,
                timestamp,
                source_ip,
                destination_ip,
                protocol,
                action,
                reason
            FROM logs
            WHERE action = ?
            ORDER BY id DESC
            LIMIT ?
        """, (
            action,
            limit
        ))

        return self.db.cursor.fetchall()

    # =====================================
    # Clear Logs
    # =====================================

    def clear_logs(self):

        self.db.cursor.execute("""
            DELETE FROM logs
        """)

        self.db.connection.commit()

    # =====================================
    # Export All Logs
    # =====================================

    def export_logs(self):

        self.db.cursor.execute("""
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
        """)

        logs = self.db.cursor.fetchall()

        filename = (
            "firewall_logs_" +
            datetime.now().strftime("%Y%m%d_%H%M%S") +
            ".csv"
        )

        filepath = os.path.abspath(filename)

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Timestamp",
                "Source IP",
                "Destination IP",
                "Protocol",
                "Action",
                "Reason"
            ])

            writer.writerows(logs)

        return filepath

    # =====================================
    # Close Database
    # =====================================

    def close(self):

        self.db.close()
