from EVE_NG.test_provisioning import (
    login,
    create_lab,
    test_add_config,
    start_nodes,
    logout,
    create_node,
    get_nodes,
    create_net,
    connect_intf,
    device_connect,
)
from EVE_NG.devices import Router
from resources import path_exists
import time
import sys
from threading import Thread

try:
    ProjectBase = sys.argv[1]
except IndexError:
    raise Exception("You need to specify a lab name!")
ProjectName = "{}".format("%20".join(ProjectBase.split()))
number_of_nodes = 10

time_before = time.time()
cookies = login()
create_lab(cookies, ProjectBase)
base_left = 20
base_top = 50

print("********** Deploying Cloud Connection... **********")
create_net(cookies, ProjectName)
print("********** Phase: Deploying Nodes... **********")
for i in range(0, number_of_nodes):
    node_id = i + 1
    hostname = f"R{node_id}"
    filepath = path_exists(hostname, "config", "4431")
    if not filepath:
        print(f"{hostname} has no configuration file! Skipping...")
        continue
    router = Router(hostname, left=base_left, top=base_top).to_json()
    create_node(cookies, router, ProjectName)
    connect_intf(cookies, ProjectName, node_id)
    time.sleep(0.1)
    with open(f"./renderedTemplates/IOS/4431/{hostname}.txt", "r") as configfile:
        config = {"data": configfile.read()}
        test_add_config(cookies, config, ProjectName, node_id)
    base_left += 40
    base_top += 50

start_nodes(cookies, ProjectName)
address_info = get_nodes(cookies, ProjectName)
logout(cookies)
mgmt_info = [
    (value["name"], value["url"]) for key, value in address_info.get("data").items()
]

print("********** Finalizing Provisioning... **********")
time.sleep(2)
threads = []
for x, device in enumerate(mgmt_info, 1):
    print(((device[1]).split(":")[1])[2:], (device[1]).split(":")[-1])
    keywords = {"auth": False}
    args = [(device[1]).split(":")[1][2:], int((device[1]).split(":")[-1]), "no\n\n"]
    th = Thread(target=device_connect, args=args, kwargs=keywords)
    th.start()
    threads.append(th)
for th in threads:
    th.join()
print("********** Done! **********")
time_after = time.time()
print(
    "********** Total Time: {} seconds **********".format(
        round(time_after - time_before, 2)
    )
)
