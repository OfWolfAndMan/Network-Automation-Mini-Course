from EVE_NG.test_provisioning import test_login, test_delete_lab, test_delete_node, test_get_nodes, test_stop_nodes
import sys

ProjectName = "{}".format("%20".join(sys.argv[1].split()))

cookies = test_login()
address_info = test_get_nodes(cookies, ProjectName)
test_stop_nodes(cookies, ProjectName)

for id in address_info.get("data"):
	x = test_delete_node(cookies, ProjectName, id)
	print(x)

test_delete_lab(cookies, ProjectName)
