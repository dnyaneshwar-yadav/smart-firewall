from scapy.all import sniff, IP, TCP, UDP
from firewall.engine import FirewallEngine
from firewall.logger import Logger


class PacketSniffer:

    def __init__(self):
        self.engine = FirewallEngine()
        self.logger = Logger()

    def process_packet(self, packet):

        # Ignore non-IP packets
        if not packet.haslayer(IP):
            return

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        protocol = "OTHER"
        port = 0

        if packet.haslayer(TCP):
            protocol = "TCP"
            port = packet[TCP].dport

        elif packet.haslayer(UDP):
            protocol = "UDP"
            port = packet[UDP].dport

        else:
            protocol = "ICMP"

        # Ask Firewall Engine
        action, reason = self.engine.analyze_packet(
            source_ip,
            port,
            protocol
        )

        # Save log into database
        self.logger.log(
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol,
            action=action,
            reason=reason
        )

        # Print packet information
        print("=" * 60)
        print(f"Source IP      : {source_ip}")
        print(f"Destination IP : {destination_ip}")
        print(f"Protocol       : {protocol}")
        print(f"Port           : {port}")
        print(f"Action         : {action}")
        print(f"Reason         : {reason}")
        print("=" * 60)

    def start(self):

        print("========================================")
        print(" Smart Firewall Started")
        print(" Monitoring Network Traffic...")
        print(" Press CTRL + C to Stop")
        print("========================================\n")

        sniff(
            prn=self.process_packet,
            store=False
        )
