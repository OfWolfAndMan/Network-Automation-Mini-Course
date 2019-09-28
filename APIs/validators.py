from cerberus import Validator
from shared.resources import yaml_function
import json

def validate_device_types(field, value, error):
	schema_file = yaml_function("./Schemas/config_policy_validators.yml", "load")
	for device_type in value:
		if device_type not in schema_file[field]['allowed']:
			error(field, f"Valid values: {[x for x in schema_file[field]['allowed']]}")

def validate_platform(field, value, error):
	schema_file = yaml_function("./Schemas/config_policy_validators.yml", "load")
	if value not in schema_file[field]['allowed']:
		error(field, f"Valid values: {[x for x in schema_file[field]['allowed']]}")


mapping_table = {"config_policy": {"file": "config_policy_validators.yml", "customValidators":
	{"platform": validate_platform, "device_types": validate_device_types}}}

def validate_schema(data, validator):
	schema_file = yaml_function(f"./Schemas/{mapping_table[validator]['file']}", "load")
	for field, myvalidator in mapping_table[validator]["customValidators"].items():
		schema_file[field]["validator"] = myvalidator
	v = Validator()
	v.validate(data, schema_file)
	if v.errors:
		return json.dumps(v.errors)

