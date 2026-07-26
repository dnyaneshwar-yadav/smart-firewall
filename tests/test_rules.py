from firewall.rules import RuleManager

manager = RuleManager()

manager.add_rule("IP", "192.168.1.100")
manager.add_rule("PORT", "80")
manager.add_rule("PROTOCOL", "ICMP")

rules = manager.get_rules()

for rule in rules:
    print(rule)

manager.close()
