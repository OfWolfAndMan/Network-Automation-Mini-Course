from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('./configTemplates/IOS'))
try:
    template = ENV.get_template("interface.j2")
    print("Template was found!")
except FileNotFoundError:
    print("The file was not found!")

class L2Interface(object):
    def __init__(self, description, intname, vlan=10, voice_vlan=20):
        self.host_description = host_description
        self.trunk_description = trunk_description
        self.intname = intname
        self.vlan = vlan
        self.voice_vlan = voice_vlan

