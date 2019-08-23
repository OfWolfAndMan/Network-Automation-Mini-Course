from jinja2 import Environment, FileSystemLoader
import os


def test_render_template(
    Hostname="R1", Template="base", Model="4431", NOS="IOS", vendor="Cisco"
):
    DirectoryToAdd = f"./renderedTemplates/{NOS}/{Model}"
    ENV = Environment(loader=FileSystemLoader(f"./configTemplates/{NOS}"))
    params = {"hostname": Hostname, "vendor": vendor, "model": Model}
    try:
        template = ENV.get_template(f"{Template}.j2")
    except FileNotFoundError:
        print(f"The template {Template} is not valid!")
    params["vendor"] = vendor
    if not os.path.exists(DirectoryToAdd):
        os.mkdir(DirectoryToAdd)

    with open(f"{DirectoryToAdd}/{Hostname}.txt", "w") as renderedTemplate:
        renderedTemplate.write(template.render(**params))
