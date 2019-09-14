from shared.resources import connect_to_api, parse_policy
from datetime import datetime

my_devices = connect_to_api("GET", "http://127.0.0.1:5005/api/v1/devices/verified/")
my_devices = my_devices.json().get("data")

my_policies = connect_to_api("GET", "http://127.0.0.1:5005/api/v1/config/compliance/")
my_policies = my_policies.json().get("data")
policy_config = {}
current = datetime.now()
print("********** Creating Compliance Report... **********")
with open(
    f"./compliance/reports/report-{current.strftime('%d-%m-%Y_%H:%M:%S')}.txt", "w"
) as file:
    file.write(
        f"**********  Compliance Report, Ran {current.strftime('%d-%m-%Y %H:%M:%S')}  **********\n\n"
    )
    for device in my_devices:
        viol_id = 1
        file.write(f"\n********** Host {device.get('deviceName')} ********** \n")
        for policy in my_policies:
            if policy.get("platform") == device.get("NOS") and device.get(
                "Role"
            ).split()[2].lower() in policy.get("device_types"):
                if policy.get("parent") != "None":
                    configPair = (policy.get("parent"), policy.get("config"))
                else:
                    configPair = (None, policy.get("config"))
                result = parse_policy(
                    configPair,
                    f"./compliance/currentConfigs/{device.get('deviceName')}.txt",
                )
                if not result:
                    file.write(
                        f"- Violation {viol_id} - {policy.get('name')} is not applied\n"
                    )
                    viol_id += 1
        connect_to_api(
            "DELETE",
            f"http://127.0.0.1:5005/api/v1/devices/verified/{device.get('deviceName')}/",
        )
        if viol_id == 1:
            file.write("No violations found!\n")
print("********** Completed! **********")
