from firewall.sniffer import PacketSniffer


def main():

    sniffer = PacketSniffer()

    sniffer.start()


if __name__ == "__main__":

    main()
