from EVE_NG.test_provisioning import test_login, test_create_lab, test_add_config, test_start_nodes, test_logout, \
	test_create_node, test_get_nodes
from EVE_NG.devices import Router
from resources import path_exists
import time
import sys

ProjectBase = sys.argv[1]
ProjectName = "{}".format("%20".join(ProjectBase.split()))
number_of_nodes = 10

cookies = test_login()
test_create_lab(cookies, ProjectBase)
base_left = 20
base_top = 50

print("Phase: Deploying Nodes...")
for i in range(0, number_of_nodes):
	node_id = 1
	hostname = f"R{i+1}"
	filepath = path_exists(hostname, 'config', '4431')
	if not filepath:
		print(f"{hostname} has no configuration file! Skipping...")
		continue
	router = (Router(hostname, left=base_left, top=base_top).to_json())
	test_create_node(cookies, router, ProjectName)
	with open(f"./renderedTemplates/IOS/4431/{hostname}.txt", 'r') as configfile:
		config = {"data": configfile.read()}
		test_add_config(cookies, config, ProjectName, node_id)
	node_id += 1
	base_left += 5
	base_top += 2

test_start_nodes(cookies, ProjectName)
address_info = test_get_nodes(cookies, ProjectName)
test_logout(cookies)
mgmt_info = [(value['name'], value['url']) for key, value in address_info.get("data").items()]

for x, device in enumerate(mgmt_info, 1):
	print(x, device)
