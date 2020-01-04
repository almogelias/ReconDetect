#####################################
'''
Class of Adapter Details + Network Finder.
'''
#####################################

from netaddr import IPAddress
from netaddr import IPNetwork


class Adapter:
    def __init__(self, name, ip, subnetMask):
        self.name = name
        self.ip = ip
        self.subnetMask = subnetMask

    def toString(self):
        try:
            print(
                "Adapter name: " + self.name + "\n" + "IP Address: " + self.ip + "\n" + "SubnetMask: " + self.subnetMask)
        except:
            print("No Adaptor")

    ### Get Network From Adapter ###
    def ipNetworkWithPrefix(self):
        try:
            prefix = IPAddress(self.subnetMask).netmask_bits()  # GetPrefix of network
            ipNetwork = IPNetwork(self.ip + "/" + str(prefix)).network  # Get NetworkAddr
            return str(ipNetwork) + "/" + str(IPAddress(self.subnetMask).netmask_bits())  # Return NetworkAddr/Prefix
        except:
            return