from resources import yaml_function
from flask import Flask

app = Flask(__name__)

@app.route('/devices/<string:device>/')
def get_device(device: str):
	"""Gets metadata for a specific device"""
	devices = yaml_function("lab_devices.yml", "load")
	for a_device in devices:
		if a_device.get("deviceName") == device:
			return a_device
	return f"Device {device} not found!"

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5005)
