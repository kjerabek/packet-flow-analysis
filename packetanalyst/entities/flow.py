import pandas as pd

class Flow:
    """
    Class wraps and aggregates packets into
    conversation.
    """

    def __init__(self, packet):
        self.packets = []
        self.packets.append(packet)
        self.flowString = packet.flowString
        self.flowStringSorted = packet.flowStringSorted
        self.src = packet.src
        self.dst = packet.dst
        self.dstp = packet.dstp
        self.srcp = packet.srcp
        self.syns = 0

    def addPacket(self, packet):
        """
        Adds packet into this flow if conversation string matches.
        Simple check, if there are two packets with syn.
        :param packet: packet
        :return: adds (True) or not (False)
        """
        if self.packets[0].flowStringSorted == packet.flowStringSorted:
            if 'flags' in packet.features['transport'].keys():
                if packet.features['transport']['flags']['syn'] == 1:

                    if self.syns < 2:
                        self.syns += 1
                    else:
                        return False

            self.packets.append(packet)
            return True
        else:
            return False

    def getDataFramePackets(self):
        """
        Extracts flow packets into pandas dataframe
        :return: dataframe of packet features
        """
        return pd.DataFrame([item.getSingleDict() for item in self.packets])

    def getPacketDirections(self):
        """
        Extract packet directions in flow.
        :return: list of up 1/down -1 direction of packets
        """
        UP = 1
        DOWN = -1
        directions = []

        upSrcIP = self.packets[0].src

        for packet in self.packets:
            if packet.src == upSrcIP:
                directions.append(UP)
            else:
                directions.append(DOWN)

        return directions

    def __iter__(self):
        for packet in self.packets:
            yield packet

    def __str__(self):
        return self.packets[0].getFlowStringSorted()
