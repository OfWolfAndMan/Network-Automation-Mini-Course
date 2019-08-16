from EVE_NG.test_provisioning import test_login, test_create_lab, test_add_config, test_start_nodes, test_logout, \
	test_create_node, test_get_nodes
from EVE_NG.devices import Router
import time
import sys

ProjectBase = sys.argv[1]
ProjectName = "{}".format("%20".join(ProjectBase.split()))
number_of_nodes = 10

cookies = test_login()
test_create_lab(cookies, ProjectBase)
base_left = 20
base_top = 50
print("Phase: Deploying Nodes")
for i in range(0, number_of_nodes):
	hostname = f"R{i+1}"
	router = (Router(hostname, left=base_left, top=base_top).to_json())
	test_create_node(cookies, router, ProjectName)
	config = '{\n\t"data": "aaa new-model\\ninterface eth0/0\\n ip address dhcp\\n no shut\\n line vty 0 4\\n transport input ssh"\n}'
	test_add_config(cookies, config, ProjectName, i+1)
	base_left += 5
	base_top += 2

test_start_nodes(cookies, ProjectName)
time.sleep(2)
address_info = test_get_nodes(cookies, ProjectName)
test_logout(cookies)
mgmt_info = [(value['name'], value['url']) for key, value in address_info.get("data").items()]
for x, device in enumerate(mgmt_info, 1):
	print(x, device)
