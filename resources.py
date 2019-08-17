import yaml
import requests
import sched
import time
import threading
import slack
import os

s = sched.scheduler(time.time, time.sleep)


def get_response_code(r):
    if r.status_code == 403:
        raise Exception("Request error! You neeed to provide authentication!")
    elif r.status_code != 200:
        raise Exception(f"An error occured! The error was {r.status_code}")
    else:
        return "Connected successfully! Pulling API response."


def connect_to_api(uri, headers=None, auth=None):
    if headers and auth:
        r = requests.get(uri, auth=auth, headers=headers)
        get_response_code(r)
    elif headers:
        r = requests.get(uri, headers=headers)
        get_response_code(r)
    elif auth:
        r = requests.get(uri, auth=auth)
        get_response_code(r)
    else:
        r = requests.get(uri)
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
    api_hostname = os.getenv("NETBOX_HOSTNAME", "127.0.0.1")
    api_port = os.getenv("NETBOX_PORT", "8080")
    r = connect_to_api(
        f"http://{api_hostname}:{api_port}/api/dcim/devices/",
        headers={"Authorization": "Token 0123456789abcdef0123456789abcdef01234567"},
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
    current_data = yaml_function("my_devices.yml", "load")

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

    yaml_function("my_devices.yml", "dump", data=current_data)


def path_exists(hostname, pathtype, model, NOS="IOS"):
    # Pathtype options: 'config' (Falls under rendered template folder), 'template'
    if pathtype == "config":
        if os.path.exists(f"./renderedTemplates/{NOS}/{model}/{hostname}.txt"):
            return True


def thread_update():
    def recurrent_update():
        while True:
            s.enter(15, 1, load_api_data)
            s.run()

    thread = threading.Thread(target=recurrent_update)
    thread.start()
