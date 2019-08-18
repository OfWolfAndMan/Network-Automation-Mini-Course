from EVE_NG.test_provisioning import (
    login,
    delete_lab,
    delete_node,
    get_nodes,
    stop_nodes,
)
import sys

ProjectName = "{}".format("%20".join(sys.argv[1].split()))

cookies = login()
address_info = get_nodes(cookies, ProjectName)
stop_nodes(cookies, ProjectName)

for id in address_info.get("data"):
    x = delete_node(cookies, ProjectName, id)
    print(x)

delete_lab(cookies, ProjectName)
