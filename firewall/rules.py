from datetime import datetime
import ipaddress
import config

from firewall.database import Database
from firewall.iptables_manager import IPTablesManager


class RuleManager:

    def __init__(self):
        self.db = Database()

    # =====================================
    # Add Rule
    # =====================================

    def add_rule(self, rule_type, value):

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.db.cursor.execute("""
        INSERT INTO rules
        (rule_type, value, status, created_at)
        VALUES (?, ?, ?, ?)
        """, (
            rule_type,
            value,
            "ACTIVE",
            created_at
        ))

        self.db.connection.commit()

    # =====================================
    # Get All Rules
    # =====================================

    def get_rules(self):

        self.db.cursor.execute("""
        SELECT *
        FROM rules
        ORDER BY id DESC
        """)

        return self.db.cursor.fetchall()

    # =====================================
    # Get Rule By ID
    # =====================================

    def get_rule(self, rule_id):

        self.db.cursor.execute("""
        SELECT *
        FROM rules
        WHERE id = ?
        """, (rule_id,))

        return self.db.cursor.fetchone()

    # =====================================
    # Delete Rule
    # =====================================

    def delete_rule(self, rule_id):

        self.db.cursor.execute("""
        DELETE FROM rules
        WHERE id = ?
        """, (rule_id,))

        self.db.connection.commit()

    # =====================================
    # Validate IP
    # =====================================

    def validate_ip(self, ip):

        try:

            ipaddress.ip_address(ip)

            protected_ips = [
                "127.0.0.1",
                "10.0.2.15"
            ]

            if ip in protected_ips:
                return False

            return True

        except ValueError:

            return False

    # =====================================
    # Validate Port
    # =====================================

    def validate_port(self, port):

        try:

            port = int(port)

            if port == 22:
                return False

            return 1 <= port <= 65535

        except ValueError:

            return False

    # =====================================
    # Validate Protocol
    # =====================================

    def validate_protocol(self, protocol):

        protocol = protocol.upper()

        allowed_protocols = [
            "TCP",
            "UDP",
            "ICMP"
        ]

        return protocol in allowed_protocols

    # =====================================
    # Apply Active Rules
    # =====================================

    def apply_rules(self):

        firewall = IPTablesManager()

        self.db.cursor.execute("""
        SELECT rule_type, value
        FROM rules
        WHERE status = 'ACTIVE'
        """)

        rules = self.db.cursor.fetchall()

        print("\n" + "=" * 60)

        if config.SIMULATION_MODE:
            print(" SMART FIREWALL - APPLY RULES (SIMULATION MODE)")
        else:
            print(" SMART FIREWALL - APPLY RULES (REAL MODE)")

        print("=" * 60)

        if not rules:

            print("No Active Rules Found.")
            print("=" * 60)
            return

        for rule_type, value in rules:

            # -----------------------------
            # IP Rule
            # -----------------------------

            if rule_type == "IP":

                if self.validate_ip(value):

                    if config.SIMULATION_MODE:
                        firewall.simulate(rule_type, value)
                    else:
                        firewall.block_ip(value)

                else:

                    print(f"SKIPPED -> Invalid / Protected IP : {value}")

            # -----------------------------
            # Port Rule
            # -----------------------------

            elif rule_type == "PORT":

                if self.validate_port(value):

                    if config.SIMULATION_MODE:
                        firewall.simulate(rule_type, value)
                    else:
                        firewall.block_port(value)

                else:

                    print(f"SKIPPED -> Invalid Port : {value}")

            # -----------------------------
            # Protocol Rule
            # -----------------------------

            elif rule_type == "PROTOCOL":

                if self.validate_protocol(value):

                    if config.SIMULATION_MODE:
                        firewall.simulate(rule_type, value)
                    else:
                        firewall.block_protocol(value)

                else:

                    print(f"SKIPPED -> Invalid Protocol : {value}")

            else:

                print(f"SKIPPED -> Unknown Rule Type : {rule_type}")

        print("=" * 60)

        if config.SIMULATION_MODE:
            print("Simulation Completed Successfully.")
        else:
            print("Firewall Rules Applied Successfully.")

        print("=" * 60)

    # =====================================
    # Close Database
    # =====================================

    def close(self):

        self.db.close()
