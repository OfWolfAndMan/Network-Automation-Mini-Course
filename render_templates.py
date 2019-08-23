from jinja2 import Environment, FileSystemLoader
import os
from configTemplates.objects import L2Interface


def render_template(Hostname, Template, Model, NOS="IOS"):
    DirectoryToAdd = f"./renderedTemplates/{NOS}/{Model}"
    ENV = Environment(loader=FileSystemLoader(f"./configTemplates/{NOS}"))
    try:
        template = ENV.get_template(f"{Template}.j2")
    except FileNotFoundError:
        print("The file was not found!")

    intf_object = L2Interface("GigabitEthernet0/", vlan=15)

    if not os.path.exists(DirectoryToAdd):
        os.mkdir(DirectoryToAdd)

    with open(f"{DirectoryToAdd}/{Hostname}.txt", "w") as renderedTemplate:
        renderedTemplate.write(template.render(interface=intf_object))
