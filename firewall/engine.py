from firewall.rules import RuleManager


class FirewallEngine:

    def __init__(self):
        self.rule_manager = RuleManager()

    def analyze_packet(self, source_ip, port, protocol):

        rules = self.rule_manager.get_rules()

        for rule in rules:

            rule_type = rule[1]
            value = rule[2]

            if rule_type == "IP" and value == source_ip:
                return "BLOCK", "Blocked IP Rule"

            if rule_type == "PORT" and value == str(port):
                return "BLOCK", "Blocked Port Rule"

            if rule_type == "PROTOCOL" and value.upper() == protocol.upper():
                return "BLOCK", "Blocked Protocol Rule"

        return "ALLOW", "No Matching Rule"

    def close(self):
        self.rule_manager.close()
