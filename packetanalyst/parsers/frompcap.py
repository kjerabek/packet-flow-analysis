from .fromfile import FromFile
import dpkt

class PcapParser(FromFile):
    """
    Class parses xml file generated by tshark.
    Extract metrics/features up to transport layer.
    TODO:
    """

    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        counter = 0

        for ts, packet in dpkt.pcap.Reader(open(self.filename, "r")):
            yield self.__extractPacketFeatures(counter, ts, packet)
            counter += 1

    def getPackets(self):
        packets = []
        counter = 0

        for ts, packet in dpkt.pcap.Reader(open(self.filename, "r")):
            packets.append(self.__extractFeaturesFromPacket(counter, ts, packet))
            counter += 1

        return packets

    def __extractFeaturesFromPacket(self, num, ts, packet):
        resPacket = {}

        eth = dpkt.ethernet.Ethernet(packet)

        resPacket['packet'] = self.__extractFeaturesFromPacket(num, ts, eth)

        resPacket['link'] = self.__extractFeaturesFromLink(eth)

        ip = eth.data
        resPacket['network'] = self.__extractFeaturesFromNetwork(ip)

        if type(eth.data) == type(dpkt.tcp.TCP()):
            tcp = ip.data
            resPacket['transport'] = {}
            resPacket['transport']['proto'] = 'tcp'
            resPacket['transport']['info'] = self.__extractFeaturesFromTcp(tcp)

        if type(eth.data) == type(dpkt.udp.UDP()):
            udp = ip.data
            resPacket['transport'] = {}
            resPacket['transport']['proto'] = 'udp'
            resPacket['transport']['info'] = self.__extractFeaturesFromTcp(udp)

        return resPacket

    def __extractFeaturesFromPcapPacketHeader(self, num, ts, pkt):
        packet = {}
        packet['size'] = len(pkt)
        packet['num'] = num
        packet['timestamp'] = ts

        return packet

    def __extractFeaturesFromLink(self, header):
        link = {}
        link['size'] = len(header)

        return link

    def __extractFeaturesFromNetwork(self, header):
        network = {}
        network['size'] = len(header)
        network['src'] = header.src
        network['dst'] = header.dst

        return network

    def __extractFeaturesFromTcp(self, header):
        tcp = {}
        tcp['flags'] = self.__extractTcpFlags(header)
        tcp['dstp'] = header.dport
        tcp['srcp'] = header.sport
        tcp['seq'] = header.seq
        tcp['ack'] = header.ack
        tcp['size'] = len(header)

        return tcp

    def __extractFeaturesFromUdp(self, header):
        udp = {}
        udp['size'] = len(header)
        udp['dstp'] = header.dport
        udp['srcp'] = header.sport

        return udp

    def __extractTcpFlags(self, flags):
        tmpFlags = {}
        tmpFlags['fin'] = (flags.flags & dpkt.tcp.TH_FIN) != 0
        tmpFlags['syn'] = (flags.flags & dpkt.tcp.TH_SYN) != 0
        tmpFlags['reset'] = (flags.flags & dpkt.tcp.TH_RST) != 0
        tmpFlags['push'] = (flags.flags & dpkt.tcp.TH_PUSH) != 0
        tmpFlags['ack'] = (flags.flags & dpkt.tcp.TH_ACK) != 0
        tmpFlags['urg'] = (flags.flags & dpkt.tcp.TH_URG) != 0
        tmpFlags['ece'] = (flags.flags & dpkt.tcp.TH_ECE) != 0
        tmpFlags['cwr'] = (flags.flags & dpkt.tcp.TH_CWR) != 0

        return tmpFlags