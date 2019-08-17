class PacketFeatures:
    """
    Class wraps stats/features data extracted from packet.
    """
    def __init__(self, features):
        self.features = features
        self.src = features['network']['src']
        self.dst = features['network']['dst']
        self.srcp = features['transport']['info']['srcp']
        self.dstp = features['transport']['info']['dstp']
        self.flowString = self.__getFlowString()
        self.flowStringSorted = self.__getFlowStringSorted()

    def __ipToHex(self, ip):
        result = ""

        for item in ip.split("."):
            result += hex(int(item))[2:]

        return result

    def __getFlowString(self):
        """
        Get tcp conversation string.
        :return: srcip-srcp_dstip-dstp
        """
        return self.src + "-" + \
                str(self.srcp) + "_" + \
                self.dst + "-" + \
                str(self.dstp)

    def __getFlowStringSorted(self):
        """
        Get tcp conversation string sorted by ip value.
        :return: srcip-srcp_dstip-dstp
        """
        if int(self.__ipToHex(self.src), 16) < int(self.__ipToHex(self.dst), 16):
            return self.src + "-" + \
                   str(self.srcp) + "_" + \
                   self.dst + "-" + \
                   str(self.dstp)
        else:
            return self.dst + "-" + \
                   str(self.dstp) + "_" + \
                   self.src + "-" + \
                   str(self.srcp)

    def getSingleDict(self):
        """
        Get one dimensional dictionary,
        keys in format "first_dimension.secon_dimension....".
        :return: one dimensional dictionary of features
        """
        return self.__getDict('', self.features)


    def __getDict(self, name, d):
        tmpDict = {}
        for key in d.keys():
            newKey = name+'.'+key if name != '' else key
            if isinstance(d[key], dict):
                tmpDict.update(self.__getDict(newKey, d[key]))
            else:
                tmpDict[newKey] = d[key]
        return tmpDict

    def __str__(self):
        return self.getFlowStringSorted()
