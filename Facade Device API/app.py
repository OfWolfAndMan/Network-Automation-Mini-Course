from resources import yaml_function
from flask import Flask, request, jsonify
import pprint

app = Flask(__name__)


@app.route("/api/v1/devices/<string:device>/")
def get_device(device: str):
    """Gets metadata for a specific device"""
    devices = yaml_function("lab_devices.yml", "load")
    for a_device in devices:
        if a_device.get("deviceName") == device:
            return a_device
    return jsonify(f"Device {device} not found!"), 404


@app.route("/api/v1/config/compliance/", methods=["GET", "POST"])
def get_config_policies():
    """Gets all config policies and creates new config policies"""
    #Example
    schema = {
        'name': 'Telnet Disable Cisco',
        'description': 'Disables telnet on Cisco devices per security requirement 1234',
        'platform': 'IOS',
        'device_types': ['router', 'switch'],
        'command': 'line vty 0 4\n no transport input telnet'
    }
    platforms = ["IOS", "IOS-XR", "NX-OS", "EOS"]
    device_types = ["router", "switch", "firewall", "load-balancer"]
    if request.method == "GET":
        config_policies = yaml_function("config_policies.yml", "load")
        return jsonify(config_policies), 200

    elif request.method == "POST":
        for field in list(request.json):
            if field not in schema.keys():
                return jsonify({"An invalid field was found! Valid fields example": schema}), 400
        if request.json["platform"] not in platforms:
            return jsonify({"An invalid platform was detected! Valid platforms": platforms}), 400
        for device_type in request.json["device_types"]:
            if device_type not in device_types:
                return jsonify({"An invalid device type was detected! Valid device types": device_types}), 400
        return {}



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
