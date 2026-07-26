import subprocess


class IPTablesManager:

    # =====================================
    # Execute Command
    # =====================================

    def run(self, command):

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )

            return True

        except subprocess.CalledProcessError as e:

            print("\n========== IPTABLES ERROR ==========")
            print(e.stderr)
            print("====================================\n")

            return False

    # =====================================
    # Block IP
    # =====================================

    def block_ip(self, ip):

        return self.run([
            "sudo",
            "iptables",
            "-A",
            "INPUT",
            "-s",
            ip,
            "-j",
            "DROP"
        ])

    # =====================================
    # Unblock IP
    # =====================================

    def unblock_ip(self, ip):

        return self.run([
            "sudo",
            "iptables",
            "-D",
            "INPUT",
            "-s",
            ip,
            "-j",
            "DROP"
        ])

    # =====================================
    # Block Port
    # =====================================

    def block_port(self, port):

        return self.run([
            "sudo",
            "iptables",
            "-A",
            "INPUT",
            "-p",
            "tcp",
            "--dport",
            str(port),
            "-j",
            "DROP"
        ])

    # =====================================
    # Unblock Port
    # =====================================

    def unblock_port(self, port):

        return self.run([
            "sudo",
            "iptables",
            "-D",
            "INPUT",
            "-p",
            "tcp",
            "--dport",
            str(port),
            "-j",
            "DROP"
        ])

    # =====================================
    # Block Protocol
    # =====================================

    def block_protocol(self, protocol):

        protocol = protocol.lower()

        return self.run([
            "sudo",
            "iptables",
            "-A",
            "INPUT",
            "-p",
            protocol,
            "-j",
            "DROP"
        ])

    # =====================================
    # Flush Firewall
    # =====================================

    def flush(self):

        try:

            subprocess.run(
                [
                    "iptables",
                    "-F"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            return True

        except subprocess.CalledProcessError as e:

            print(e.stderr)

            return False

    # =====================================
    # List Firewall Rules
    # =====================================

    def list_rules(self):

        try:

            result = subprocess.run(
                [
                    "iptables",
                    "-L",
                    "--line-numbers",
                    "-n"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            if result.stdout.strip():

                return result.stdout

            return "No Active Firewall Rules."

        except subprocess.CalledProcessError as e:

            return (
                "Permission denied while reading firewall rules.\n\n"
                "Run Flask with appropriate privileges or configure "
                "sudoers for iptables.\n\n"
                f"{e.stderr}"
            )

        except Exception as e:

            return f"Error : {e}"

    # =====================================
    # Simulation Mode
    # =====================================

    def simulate(self, rule_type, value):

        print("=" * 50)

        if rule_type == "IP":

            print(f"SIMULATION : BLOCK IP -> {value}")

        elif rule_type == "PORT":

            print(f"SIMULATION : BLOCK PORT -> {value}")

        elif rule_type == "PROTOCOL":

            print(f"SIMULATION : BLOCK PROTOCOL -> {value}")

        else:

            print(f"UNKNOWN RULE : {rule_type}")

        print("=" * 50)
