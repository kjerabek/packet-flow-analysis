from .parsers.fromxmlpcap import XmlPcapParser
from .parsers.frompcap import PcapParser
from .entities.flow import Flow
import pandas as pd

class ExtractorError(Exception):
    pass

class PacketExtractor:
    """
    Class wraps file parsers and extracts packet fetures from
    specified file and group them into flows.
    """


    def __init__(self, filename):
        self.packets = []
        self.flows = []
        self.filename = filename

        fileFormat = filename.split(".")[-1].lower()

        if fileFormat == "xml":
            self.parser = XmlPcapParser

        elif "cap" in fileFormat:
            self.parser = PcapParser

        else:
            raise ExtractorError("Unsupported file format {}".format(fileFormat))

    def __initExtractor(self):
        self.extractor = self.parser(self.filename)

    def extractPackets(self):
        """
        Extracts all packets from specified file.
        :return: extracted packet list
        """
        self.__initExtractor()
        self.packets = self.extractor.getPackets()

        return self.packets

    def extractPacketsLimited(self, num):
        """
        Extracts all packets up to num from specified file.
        :param num: number of packets to be extracted
        :return: extracted packets
        """
        self.__initExtractor()
        counter = 0
        tmpPackets = []

        for packet in self.extractor:
            if counter == num-1:
                break

            tmpPackets.append(packet)
            counter += 1

        self.packets = tmpPackets

        return tmpPackets

    def getFlows(self):
        """
        Group packets into flows by sorted flow string,
        just simple check if packet belongs to flow by syn flag.
        TODO: better check
        :return: list of flows
        """
        self.flows = []

        indexCounter = 0
        tmpFlowMapping = {}

        for packet in self.packets:
            if packet.flowStringSorted in tmpFlowMapping.keys():
                if not self.flows[tmpFlowMapping[packet.flowStringSorted]].addPacket(packet):
                    tmpFlowMapping[packet.flowStringSorted] = indexCounter
                    indexCounter += 1
                    self.flows.append(Flow(packet))
            else:
                tmpFlowMapping[packet.flowStringSorted] = indexCounter
                indexCounter += 1
                self.flows.append(Flow(packet))


        return self.flows

    def getDataFramePackets(self):
        """
        Get all packets from file into pandas DataFrame
        :return: dataframe with packetfeatures
        """
        return pd.DataFrame([item.getSingleDict() for item in self.packets])

    def extractStatisticsFromDataFrame(self, source):
        if not isinstance(source, pd.DataFrame):
            return None

        stats = {}
        payloadSize = source['payload.size'].describe(include="all")
        packetSize = source['packet.size'].describe(include="all")

        stats['packet.size.min'] = packetSize['min']
        stats['packet.size.max'] = packetSize['max']
        stats['packet.size.std'] = packetSize['std']
        stats['packet.size.mean'] = packetSize['mean']
        stats['packet.size.sum'] = source['packet.size'].sum()

        stats['payload.size.min'] = payloadSize['min']
        stats['payload.size.max'] = payloadSize['max']
        stats['payload.size.std'] = payloadSize['std']
        stats['payload.size.mean'] = payloadSize['mean']
        stats['payload.size.sum'] = source['payload.size'].sum()

        stats['payload.size.0count'] = source['payload.size'].value_counts()[0]
        stats['packet.count'] = len(source)

        if source['transport.proto'][0] == 'tcp':
            stats['tcp.flags.push.count'] = source['transport.info.flags.push'].sum()
            stats['tcp.flags.ns.count'] = source['transport.info.flags.ns'].sum()
            stats['tcp.flags.cwr.count'] = source['transport.info.flags.cwr'].sum()
            stats['tcp.flags.ecn.count'] = source['transport.info.flags.ecn'].sum()
            stats['tcp.flags.urg.count'] = source['transport.info.flags.urg'].sum()
            stats['tcp.flags.ack.count'] = source['transport.info.flags.ack'].sum()
            stats['tcp.flags.push.count'] = source['transport.info.flags.push'].sum()
            stats['tcp.flags.reset.count'] = source['transport.info.flags.reset'].sum()
            stats['tcp.flags.syn.count'] = source['transport.info.flags.syn'].sum()
            stats['tcp.flags.fin.count'] = source['transport.info.flags.fin'].sum()

        return stats
