from provisioning import (
    login,
    delete_lab,
    delete_node,
    get_nodes,
    stop_nodes,
    delete_net,
)
import sys

try:
    ProjectName = "{}".format("%20".join(sys.argv[1].split()))
except IndexError:
    raise Exception("You need to specify a lab name!")

cookies = login()
address_info = get_nodes(cookies, ProjectName)
print("********** Stopping Nodes... **********")
stop_nodes(cookies, ProjectName)
print("********** Deleting Networks... **********")
delete_net(cookies, ProjectName, 1)

if address_info.get("data"):
    for id in address_info.get("data"):
        x = delete_node(cookies, ProjectName, id)

delete_lab(cookies, ProjectName)
