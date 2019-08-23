from render_templates import render_template
from resources import yaml_function

devices = yaml_function("APIs/lab_devices.yml", "load")

for device in devices:
    render_template(
        device.get("deviceName"),
        "interface",
        device.get("Model"),
        int_prefix="GigabitEthernet0/",
        vlan=15,
    )

# breakpoint() - builtin function to replace pdb
