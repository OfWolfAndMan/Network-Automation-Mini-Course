import yaml
import requests
import sched
import time
import threading
import slack
import os

s = sched.scheduler(time.time, time.sleep)


def get_response_code(r):
    if 40 in r.status_code:
        raise Exception(r.json())
    elif 50 in r.status_code:
        raise Exception(r.json())
    elif 30 in r.status_code:
        raise Exception(r.json())
    elif 20 not in r.status_code:
        raise Exception(f"An error occured! The error was {r.status_code}")


def connect_to_api(
    method, uri, headers=None, auth=None, data=None, json=None, cookies=None
):
    methods = ["GET", "PUT", "PATCH", "DELETE", "POST"]
    if method not in methods:
        raise ValueError("Not a valid HTTP method!")
    if headers and auth:
        r = requests.request(method, uri, auth=auth, headers=headers)
        get_response_code(r)
    elif headers:
        r = requests.request(method, uri, headers=headers)
        get_response_code(r)
    elif data:
        r = requests.request(method, uri, data=data)
        get_response_code(r)
    elif headers and data:
        r = requests.request(method, uri, headers=headers, data=data)
        get_response_code(r)
    elif headers and data and auth:
        r = requests.request(method, uri, headers=headers, auth=auth, data=data)
        get_response_code(r)
    elif headers and json:
        r = requests.request(method, uri, headers=headers, json=json)
        get_response_code(r)
    elif cookies and headers and json:
        r = requests.request(method, uri, headers=headers, json=json, cookies=cookies)
        get_response_code(r)
    elif auth:
        r = requests.request(method, uri, auth=auth)
        get_response_code(r)
    else:
        r = requests.request(method, uri)
        get_response_code(r)
    return r.json()


def yaml_function(file, operation, data=None):
    if operation == "dump":
        with open(file, "w") as yaml_file:
            yaml.dump(data, yaml_file)
    elif operation == "load":
        with open(file, "r") as yaml_file:
            new_data = yaml.load(yaml_file, Loader=yaml.BaseLoader)
            return new_data
    else:
        raise Exception(f"{operation} is not a valid YAML operation!")


def send_slack(hostname, type, address):
    client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])

    client.chat_postMessage(
        channel="automatedmessage",
        text=f"{hostname} {type} instance has been changed -  {address}",
    )


def load_api_data():
    """Can use Netbox API"""
    api_hostname = os.getenv("API_HOSTNAME", "127.0.0.1")
    api_port = os.getenv("API_PORT", "8080")
    """Supplying Auth token as an env variable is REQUIRED"""
    api_auth = os.getenv("API_AUTH", None)
    r = requests.request(
        "GET", f"http://{api_hostname}:{api_port}/api/dcim/devices/", headers=api_auth
    )

    my_devices = []
    for result in r["results"]:
        vendor = result.get("device_type").get("manufacturer").get("name")
        model = result.get("device_type").get("model")
        device = result.get("name")
        if result.get("primary_ip4"):
            mgmt_ip = result.get("primary_ip4").get("address")
        else:
            mgmt_ip = None
        role = result.get("device_role").get("name")
        region = result.get("config_context").get("region")
        site = result.get("site").get("name")
        tacacs = result.get("config_context").get("tacacs_server")
        my_devices.append(
            {
                "Vendor": vendor,
                "Model": model,
                "deviceName": device,
                "Management IP": mgmt_ip,
                "Role": role,
                "Region": region,
                "Site": site,
                "TACACS Server": tacacs,
            }
        )
    current_data = yaml_function("APIs/lab_devices.yml", "load")

    for device in my_devices:
        for x, current_device in enumerate(current_data):
            for key, value in current_device.items():
                if current_device[key] == "null" and device[key] is None:
                    pass
                elif (
                    current_device["deviceName"] == device["deviceName"]
                    and current_device[key] != device[key]
                ):
                    current_data[x][key] = device[key]
                    if key.lower() == "tacacs server":
                        send_slack(current_device["deviceName"], "tacacs", device[key])

    yaml_function("APIs/lab_devices.yml", "dump", data=current_data)


def thread_update():
    def recurrent_update():
        while True:
            s.enter(15, 1, load_api_data)
            s.run()

    thread = threading.Thread(target=recurrent_update)
    thread.start()
