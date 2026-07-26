from firewall.engine import FirewallEngine

engine = FirewallEngine()

action, reason = engine.analyze_packet(
    source_ip="10.10.10.10",
    port=8080,
    protocol="TCP"
)

print("Action :", action)
print("Reason :", reason)

engine.close()
