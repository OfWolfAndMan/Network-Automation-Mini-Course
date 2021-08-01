from netmiko import ConnectHandler
import asyncio
from datetime import datetime
import logging

# logging.basicConfig(level=logging.DEBUG)

def main():
	loop = asyncio.get_event_loop()
	devices = asyncio.Queue()
	input_inv = ["192.168.170.151", "192.168.170.152", "192.168.170.153", "192.168.170.154", "192.168.170.155"]
	begin = datetime.now()
	connect_devices = loop.create_task(populate_devices(input_inv, devices))
	output = loop.create_task(get_output(devices))
	main_task = asyncio.gather(connect_devices, output)
	loop.run_until_complete(main_task)
	end = datetime.now()
	print(f"Total time elapsed: {(end - begin).seconds} seconds")

async def populate_devices(inventory: list, devices: asyncio.Queue):
	await devices.put(inventory.pop())

async def get_output(devices):
	my_device = await devices.get()
	device = Router(my_device, "admin", "cisco", "cisco_ios")
	device.connect()
	output = device.send_command("show run | section line")
	print(output)
	device.disconnect()


class Device:
	# defining constructor
	def __init__(self, host, username, password, device_type, port=22):
		self._connect_params = {
			"host": host,
			"username": username,
			"password": password,
			"port": port,
			"device_type": device_type
		}

	# defining class methods
	def connect(self):
		connection = ConnectHandler(**self._connect_params)
		self.connection = connection
		return connection

	def disconnect(self):
		self.connection.disconnect()

	# end of class definition

class Router(Device):
	def __init__(self, host, username, password, device_type):
		super().__init__(host, username, password, device_type)

	def send_command(self, command):
		response = self.connection.send_command(command)
		return response

main()
