from shared.resources import connect_to_api
from shared.storage import NOSes, connect_mapping_table
from EVE_NG.config_collector import collect_device_configs, create_threads

my_devices = connect_to_api("GET", "http://127.0.0.1:5005/api/v1/devices/")
my_devices = my_devices.json().get("data")


print("********** Collecting Device Configs... **********")
for device in my_devices:
	threads = []
	create_threads(collect_device_configs, threads,
		device.get("deviceName"),
		device.get("Management IP").split('/')[0],
		22,
		"show run\n",
		user="admin",
		password="mysecret",
		device_type=connect_mapping_table[device.get("NOS")],
	)

