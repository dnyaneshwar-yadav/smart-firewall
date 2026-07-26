from firewall.logger import Logger

logger = Logger()

logger.log(
    source_ip="192.168.1.100",
    destination_ip="8.8.8.8",
    protocol="ICMP",
    action="BLOCK",
    reason="Blocked IP Rule"
)

logger.close()

print("Log Inserted Successfully!")
