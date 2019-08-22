from jinja2 import Environment, FileSystemLoader
import os


def render_template(Hostname, Template, Model, NOS="IOS"):
    DirectoryToAdd = f"./renderedTemplates/{NOS}/{Model}"
    ENV = Environment(loader=FileSystemLoader(f"./configTemplates/{NOS}"))
    try:
        template = ENV.get_template(f"{Template}.j2")
    except FileNotFoundError:
        print("The file was not found!")

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

    intf_object = L2Interface("GigabitEthernet0/", vlan=15)

    if not os.path.exists(DirectoryToAdd):
        os.mkdir(DirectoryToAdd)

    with open(f"{DirectoryToAdd}/{Hostname}.txt", "w") as renderedTemplate:
        renderedTemplate.write(template.render(interface=intf_object))
