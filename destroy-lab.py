from EVE_NG.test_provisioning import (
    login,
    delete_lab,
    delete_node,
    get_nodes,
    stop_nodes,
    delete_net,
)
import sys

ProjectName = "{}".format("%20".join(sys.argv[1].split()))

cookies = login()
address_info = get_nodes(cookies, ProjectName)
print("********** Stopping Nodes... **********")
stop_nodes(cookies, ProjectName)
print("********** Deleting Networks... **********")
delete_net(cookies, ProjectName, 1)

for id in address_info.get("data"):
    x = delete_node(cookies, ProjectName, id)

delete_lab(cookies, ProjectName)
