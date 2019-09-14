from jinja2 import Environment, FileSystemLoader
import os
from configTemplates.objects import L2Interface


def render_template(
    Hostname, Template, Model=None, NOS="IOS", vendor="Cisco", **kwargs
):
    ENV = Environment(loader=FileSystemLoader(f"./configTemplates/{NOS}"))
    params = {"hostname": Hostname, "vendor": vendor, "model": Model}
    try:
        template = ENV.get_template(f"{Template}.j2")
    except FileNotFoundError:
        print(f"The template {Template} is not valid!")

    if Template != "initial":
        if not Model:
            raise Exception("Need to specify model!")
        if Template == "interface":
            intf_object = L2Interface(kwargs["int_prefix"], kwargs["vlan"])
            params["interface"] = intf_object
        elif Template == "compliance":
            pass
        DirectoryToAdd = f"./renderedTemplates/{NOS}/{Model}"
        if not os.path.exists(DirectoryToAdd):
            os.mkdir(DirectoryToAdd)

        with open(f"{DirectoryToAdd}/{Hostname}.txt", "w") as renderedTemplate:
            renderedTemplate.write(template.render(**params))
    else:
        Directory = f"./renderedTemplates/deployment"
        params["mgmt_ip"] = kwargs["mgmt_ip"]
        with open(f"{Directory}/{Hostname}.txt", "w") as renderedTemplate:
            renderedTemplate.write(template.render(**params))
