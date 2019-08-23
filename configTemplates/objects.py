class L2Interface(object):
    def __init__(
        self,
        intname,
        trunk_description="<===Trunk Port===>",
        host_description="<===User Port===>",
        vlan=10,
        voice_vlan=20,
    ):
        self.trunk_description = trunk_description
        self.host_description = host_description
        self.intname = intname
        self.vlan = vlan
        self.voice_vlan = voice_vlan


class L3Interface(object):
    def __init__(self, intname, subnet, mask, description="<===Uplink===>"):
        self.description = description
        self.subnet = subnet
        self.mask = mask
        self.intname = intname


class Router(object):
    def __init__(self, hostname):
        self.hostname = hostname
