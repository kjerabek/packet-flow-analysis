import sys
import requests
import dnslib
import base64
import argparse

class DOHRequests:
    headers = {"Accept": "application/dns-message",
                "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
                "Content-Type": "application/dns-message"}


    def __init__(self, dnsreqtype, httpreqtype, wireorjson, url=None,
                 inputfilename=None, outputfilename=None):

        self.inputfilename = inputfilename
        self.dnsreqtype = dnsreqtype
        self.httpreqtype = httpreqtype
        self.wireorjson = wireorjson
        self.outputfilename = outputfilename

        if self.outputfilename:
            self.output = open(self.outputfilename, 'w')
        else:
            self.output = sys.stdout

        if url:
            self.url = url
        else:
            self.url = "https://cloudflare-dns.com/dns-query"

    def createDnsWireQuery(self, domain):
        dnsWireQuery = dnslib.DNSRecord.question(domain, dnsreqtype)
        dnsWireQuery.header.id = 0

        return dnsWireQuery

    def getJson(self, domain):
        headers["Accept"] = "application/dns-json"
        url += "?name={}&type={}".format(domain, dnsreqtype)

        result = requests.get(url,
                              headers=self.headers)

        self.output.write("#"+domain+"\n")
        self.output.write(result.text+"\n")

    def getWire(self, domain):
        dnsWireQuery = self.createDnsWireQuery(domain)
        url += "?dns=" +
                str(base64.urlsafe_b64encode(dnsWireQuery.pack()))[2:-1].replace("=", "")

        result = requests.get(url,
                              headers=self.headers)

        self.output.write("#"+domain+"\n")
        if len(result.content) > 0:
            self.output.write(str(dnslib.DNSRecord.parse(result.content))+"\n")

    def postWire(self, domain):
        dnsWireQuery = self.createDnsWireQuery(domain)
        data = dnsWireQuery.pack()

        result = requests.post(url,
                               data=data,
                               headers=self.headers)

        self.output.write("#"+domain+"\n")
        if len(result.content) > 0:
            self.output.write(str(dnslib.DNSRecord.parse(result.content))+"\n")

    def makeRequest(self, domain):
        if self.wireorjson == "json":
            if self.httpreqtype == "GET":
                self.getJson(domain)
            elif self.httpreqtype == "POST":
                raise Exception("Bad request type POST can accept only wire formated message")

        elif self.wireorjson == "wire":
            if self.httpreqtype == "GET":
                self.getWire(domain)
            elif self.httpreqtype == "POST":
                self.postWire(domain)

    def makeRequests(self):
        counter = 0

        try:
            for line in open(self.inputfilename, "r"):
                domain = line.strip()
                print("{}: {}".format(counter, domain))

                self.makeRequest(domain)
                counter+=1
        except:
            print("Enter input filename")

    def __del__(self):
        self.output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description='Application do requests for DOH')

    parser.add_argument('-i', '--input-file',
                        action="store",
                        dest="inputfilename",
                        default=None)

    parser.add_argument('-o', '--output-file',
                        action="store",
                        dest="outputfilename",
                        default=None)

    parser.add_argument('-d', '--dns-request-type',
                        action="store",
                        dest="dnsreqtype",
                        choices=["A", "AAAA", "MX", "TXT"],
                        default="A")

    parser.add_argument('-t', '--http-request-type',
                        action="store",
                        dest="httpreqtype",
                        choices=["GET", "POST"],
                        default="GET")

    parser.add_argument('-w', '--wire-or-json',
                        action="store",
                        dest="wireorjson",
                        choices=["wire", "json"],
                        default="json")

    parser.add_argument('-u', '--url',
                        action="store",
                        dest="url",
                        default="https://cloudflare-dns.com/dns-query")

    parser.add_argument('domain',
                        action="store",
                        nargs="?",
                        default=None)

    args = parser.parse_args()

    doh = DOHRequests(args.dnsreqtype,
                      args.httpreqtype,
                      args.wireorjson,
                      args.url,
                      args.inputfilename,
                      args.outputfilename)
