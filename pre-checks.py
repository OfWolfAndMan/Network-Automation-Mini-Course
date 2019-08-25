from shared.resources import connect_to_api
from shared.storage import NOSes, all_devices
from EVE_NG.provisioning import device_connect

for device in all_devices:
	if device.get("NOS") not in NOSes:
		NOSes.append(device.get("NOS"))

for device in all_devices:
	device_connect(
		device.get("deviceName"),
		22,
		"show run\n",
		user="admin",
		password="mysecret",
		device_type="cisco_ios",
		auth=True,
	)

my_policies = connect_to_api("GET", "http://127.0.0.1:5005/api/v1/config/compliance/")

