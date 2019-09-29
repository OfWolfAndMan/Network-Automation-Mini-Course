from flask import Flask, request, jsonify
from secrets import token_hex
import json

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "APIs"
from shared.resources import yaml_function
from APIs.validators import validate_schema

app = Flask(__name__)

verifiedDevices = []


@app.route("/api/v1/devices/")
def get_devices():
    """Gets metadata for a specific device"""
    devices = yaml_function("./lab_devices.yml", "load")
    return jsonify({"data": devices}), 200


@app.route("/api/v1/devices/<string:device>/", methods=["GET", "POST"])
def get_device(device: str):
    """Gets metadata for a specific device"""
    if request.method == "GET":
        devices = yaml_function("./APIs/lab_devices.yml", "load")
        for a_device in devices:
            if a_device.get("deviceName") == device:
                return jsonify({"data": a_device}), 200
        return jsonify({"error": f"Device {device} not found!"}), 404
    elif request.method == "POST":
        invalid_schema = validate_schema(request.json, "lab_devices")
        if invalid_schema:
            return jsonify(json.loads(invalid_schema)), 400
        if len(request.json) != 9:
            return jsonify({"The number of parameters you specified is invalid!"}), 400
        data = yaml_function("./lab_devices.yml", "load")
        for entry in data:
            if entry["deviceName"].lower() == request.json["deviceName"].lower():
                return jsonify({"error": "Device already exists!"}), 200
        new_data = request.json
        data.append(new_data)
        yaml_function("./lab_devices.yml", "dump", data=data)
        return jsonify({"data": request.json}), 201


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


@app.route("/api/v1/devices/verified/<string:device>/", methods=["DELETE"])
def delete_verified_device(device: str):
    """Deletes a device that is reachable"""
    newVerifiedDevices = verifiedDevices
    for my_device in newVerifiedDevices:
        if my_device.get("deviceName") == device:
            verifiedDevices.remove(my_device)
            return jsonify({}), 204
    return jsonify({"error": f"Device {device} not in verified devices!"}), 404


@app.route("/api/v1/config/compliance/", methods=["GET", "POST"])
def get_config_policies():
    """Gets all config policies and creates new config policies"""
    schema = {
        "name": "Telnet Disable Cisco",
        "description": "Disables telnet on Cisco devices per security requirement 1234",
        "platform": "IOS",
        "device_types": ["router", "switch"],
        "config": "no transport input telnet",
        "parent": "line vty 0 4",
    }
    if request.method == "GET":
        config_policies = yaml_function("./APIs/config_policies.yml", "load")
        return jsonify({"data": config_policies}), 200

    elif request.method == "POST":
        invalid_schema = validate_schema(request.json, "config_policy")
        if invalid_schema:
            return jsonify(json.loads(invalid_schema)), 400
        if len(request.json) != 6:
            return (
                jsonify(
                    {
                        "The number of parameters you specified is invalid! Valid fields example": schema
                    }
                ),
                400,
            )
        data = yaml_function("./config_policies.yml", "load")
        for entry in data:
            if (
                entry["name"].lower() == request.json["name"].lower()
                and entry["platform"].lower() == request.json["platform"].lower()
            ):
                return jsonify({"error": "Configuration policy already exists!"}), 200
        new_data = request.json
        new_data["id"] = token_hex(16)
        data.append(new_data)
        yaml_function("./config_policies.yml", "dump", data=data)
        return jsonify({"data": request.json}), 201


@app.route("/api/v1/config/compliance/<string:id>/", methods=["DELETE"])
def delete_config_policy(id: str):
    """Deletes config compliance policy based on its respective id"""
    config_policies = yaml_function("./APIs/config_policies.yml", "load")
    for policy in config_policies:
        if policy.get("id") == id:
            config_policies.remove(policy)
            yaml_function("./APIs/config_policies.yml", "dump", data=config_policies)
            return jsonify({}), 200
    return jsonify({"error": f"Config policy ID {id} not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
