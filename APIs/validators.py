from cerberus import Validator
from shared.resources import yaml_function
import json
import re
from ipaddress import ip_address


def validate_ip_address(address):
    """
    Validate address is either an IPv4 or IPv6 address.
    :param address: String - IPv4 or IPv6 address
    :return: Int - 0, 4 or 6
    """
    if not isinstance(address, str):
        return 0
    try:
        return ip_address(address).version
    except ValueError:
        return 0


class CustomValidator(Validator):
    """
    Add type checking for network related fields.
    """

    def _validate_type_ipv4_address(self, value):
        """
        Check the value is a valid IPv4 address
        :param value: String - IPv4 Address
        :return: Bool
        """
        if validate_ip_address(value) == 4:
            return True

    def _validate_type_ipv6_address(self, value):
        """
        Check the value is a valid IPv6 address
        :param value: String - IPv4 Address
        :return: Bool
        """
        if validate_ip_address(value) == 6:
            return True

    def _validate_type_mac_address(self, value):
        """
        Check the value is a valid MAC address.
        Valid format: 00:11:22:aa:bb:cc
        :param value: String - MAC address in unix format
        :return: Bool
        """
        try:
            if bool(re.match("([a-fA-F0-9]{2}[:]){5}([a-fA-F0-9]{2})", value)):
                return True
        except TypeError:
            pass


def validate_device_types(field, value, error):
    schema_file = yaml_function("./Schemas/config_policy_validators.yml", "load")
    for device_type in value:
        if device_type not in schema_file[field]["allowed"]:
            error(field, f"Valid values: {[x for x in schema_file[field]['allowed']]}")


def validate_platform(field, value, error):
    schema_file = yaml_function("./Schemas/config_policy_validators.yml", "load")
    if value not in schema_file[field]["allowed"]:
        error(field, f"Valid values: {[x for x in schema_file[field]['allowed']]}")


mapping_table = [
    {
        "config_policy": {
            "file": "config_policy_validators.yml",
            "customValidators": {
                "platform": validate_platform,
                "device_types": validate_device_types,
            },
        }
    },
    {"lab_devices": {"file": "lab_devices_validators.yml", "customValidators": {}}},
]


def validate_schema(data, validator):
    for num, mapping in enumerate(mapping_table):
        if mapping.get(validator):
            schema_file = yaml_function(
                f"./Schemas/{mapping_table[num][validator]['file']}", "load"
            )
            for field, myvalidator in mapping_table[num][validator][
                "customValidators"
            ].items():
                schema_file[field]["validator"] = myvalidator
    v = CustomValidator()
    v.validate(data, schema_file)
    if v.errors:
        return json.dumps(v.errors)
