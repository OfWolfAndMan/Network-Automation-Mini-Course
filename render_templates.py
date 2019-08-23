from jinja2 import Environment, FileSystemLoader
import os
from configTemplates.objects import L2Interface


def render_template(Hostname, Template, Model, NOS="IOS", vendor="Cisco", **kwargs):
    DirectoryToAdd = f"./renderedTemplates/{NOS}/{Model}"
    ENV = Environment(loader=FileSystemLoader(f"./configTemplates/{NOS}"))
    params = {"hostname": Hostname, "vendor": vendor, "model": Model}
    try:
        template = ENV.get_template(f"{Template}.j2")
    except FileNotFoundError:
        print(f"The template {Template} is not valid!")

    if Template == 'interface':
        intf_object = L2Interface(kwargs['int_prefix'], kwargs['vlan'])
        params["interface"] = intf_object
    elif Template == 'compliance':
        pass

    if not os.path.exists(DirectoryToAdd):
        os.mkdir(DirectoryToAdd)

    with open(f"{DirectoryToAdd}/{Hostname}.txt", "w") as renderedTemplate:
        renderedTemplate.write(template.render(**params))
