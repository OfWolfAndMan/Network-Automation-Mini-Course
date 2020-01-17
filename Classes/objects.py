from netmiko import ConnectHandler

class NetworkDevice:
	def __init__(self, ip_address, username, password):
		self.ip_address = ip_address
		self.username = username
		self.password = password
		self.port = 22

	def get_info(self, model):
		print(f"The IP address of this device is {self.ip_address} and the username of the device is {self.username} and the model is {model}")

	def connect(self, device_type):
		x = ConnectHandler(host=self.ip_address, username=self.username, password=self.password, device_type=device_type)
		self.connection = x

	def get_output(self, command):
		if self.connection:
			output = self.connection.send_command(command)
			return output
		else:
			return "No connection to run command!"

	def disconnect(self):
		if self.connection:
			self.connection.disconnect()
		else:
			return "No connection to disconnect!"


class Router(NetworkDevice):
	def __init__(self, ip_address, username, password):
		super().__init__(ip_address, username, password)
		# self.license = License(license_name, license_expiration)

	def get_prompt(self):
		if self.connection:
			prompt = self.connection.find_prompt()
			return prompt
		else:
			return "No connection to receive prompt from!"

	# def get_info(self, model):
	# 	print(f"The model is {model} and the license is {self.license.license_name}")

class License:
	def __init__(self, license_name, expiration):
		self.expiration = expiration
		self.license_name = license_name

	def get_license_details(self):
		print(f"The license for this device is {self.license_name} and the expiration is {self.expiration}")

router = Router("192.168.170.151", "admin", "cisco")
router.connect("cisco_ios")
print(router.get_prompt())
router.disconnect()
