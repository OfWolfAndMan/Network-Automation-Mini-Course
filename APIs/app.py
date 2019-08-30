from flask import Flask, request, jsonify
from secrets import token_hex

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "APIs"
from shared.resources import yaml_function

app = Flask(__name__)

verifiedDevices = []

@app.route("/api/v1/devices/")
def get_devices():
    """Gets metadata for a specific device"""
    devices = yaml_function("./APIs/lab_devices.yml", "load")
    return jsonify({"data": devices}), 200

@app.route("/api/v1/devices/<string:device>/")
def get_device(device: str):
    """Gets metadata for a specific device"""
    devices = yaml_function("./APIs/lab_devices.yml", "load")
    for a_device in devices:
        if a_device.get("deviceName") == device:
            return jsonify({"data": a_device}), 200
    return jsonify({"error": f"Device {device} not found!"}), 404

@app.route("/api/v1/devices/verified/", methods=["GET", "POST"])
def get_verified_devices():
    """Gets all devices that are reachable"""
    # Example
    if request.method == "GET":
        return jsonify({"data": verifiedDevices}), 200

    elif request.method == "POST":
        new_data = request.json
        verifiedDevices.append(new_data)
        return jsonify({"data": verifiedDevices}), 201


@app.route("/api/v1/config/compliance/", methods=["GET", "POST"])
def get_config_policies():
    """Gets all config policies and creates new config policies"""
    # Example
    schema = {
        "name": "Telnet Disable Cisco",
        "description": "Disables telnet on Cisco devices per security requirement 1234",
        "platform": "IOS",
        "device_types": ["router", "switch"],
        "config": "no transport input telnet"
    }
    platforms = ["IOS", "IOS-XR", "NX-OS", "EOS"]
    device_types = ["router", "switch", "firewall", "load-balancer"]
    if request.method == "GET":
        config_policies = yaml_function("./APIs/config_policies.yml", "load")
        return jsonify({"data": config_policies}), 200

    elif request.method == "POST":
        if len(request.json) != 5:
            return jsonify({"A required field is missing! Valid fields": schema}), 400
        for field in list(request.json):
            if field not in schema.keys():
                return (
                    jsonify(
                        {"An invalid field was found! Valid fields example": schema}
                    ),
                    400,
                )
        if request.json["platform"].upper() not in platforms:
            return (
                jsonify(
                    {"An invalid platform was detected! Valid platforms": platforms}
                ),
                400,
            )
        for device_type in request.json["device_types"]:
            if device_type.lower() not in device_types:
                return (
                    jsonify(
                        {
                            "An invalid device type was detected! Valid device types": device_types
                        }
                    ),
                    400,
                )
        data = yaml_function("./APIs/config_policies.yml", "load")
        for entry in data:
            if (
                entry["name"].lower() == request.json["name"].lower()
                and entry["platform"].lower() == request.json["platform"].lower()
            ):
                return jsonify({"error": "Configuration policy already exists!"}), 200
        new_data = request.json
        new_data["id"] = token_hex(16)
        data.append(new_data)
        yaml_function("./APIs/config_policies.yml", "dump", data=data)
        return jsonify({"data": request.json}), 201


@app.route("/api/v1/config/compliance/<string:id>/", methods=["DELETE"])
def delete_config_policy(id: str):
    """Deletes config compliance policy based on its respective id"""
    config_policies = yaml_function("./APIs/config_policies.yml", "load")
    for policy in config_policies:
        if policy.get("id") == id:
            config_policies.remove(policy)
            return jsonify({}), 200
    return jsonify({"error": f"Config policy ID {id} not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
