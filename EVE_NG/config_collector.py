from EVE_NG.provisioning import device_connect
from threading import Thread

def create_threads(func, threads, *args, **keywords):
	kwargs = {}
	for key, value in keywords.items():
		kwargs[key] = value
	th = Thread(target=func, args=args, kwargs=kwargs)
	th.start()
	threads.append(th)

	for th in threads:
		th.join()


def collect_device_configs(hostname, mgmt_ip, port, command, user=None, password=None, device_type=None):
	output = device_connect(
		mgmt_ip,
		port,
		command,
		user=user,
		password=password,
		device_type=device_type,
	)
	with open(f"./compliance/currentConfigs/{hostname}.txt", "w") as file:
		file.write(output)
