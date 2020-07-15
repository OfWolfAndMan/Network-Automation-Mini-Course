from ntc_templates.parse import parse_output
import os
import csv

BASE_PATH = "./config/"

def csv_writer(output_file: str, fieldnames: list, BASE_PATH: str, command: str, platform: str) -> None:
	"""
	Writes parsed information into a csv file, based on the command and fields of interest given

	:param output_file: The file which will store the select information from the parsed output
	:param fieldnames: The fields to be stored in the csv file
	:param BASE_PATH: The base path to the parsed outputs
	:param command: The expected network command to be parsed
	:param platform: The platform of our network device (i.e. cisco_ios, cisco_nxos)
	:return: None
	"""
	try:
		with open(output_file, 'w', newline='\n') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for file in os.listdir(BASE_PATH):
				file = open(BASE_PATH + file)
				config = file.read()
				inventory_parsed = parse_output(platform=platform, command=command, data=config)
				inv_fixed = {k: v for k, v in inventory_parsed[0].items() if k in fieldnames}
				writer.writerow(inv_fixed)
	except FileNotFoundError as e:
		print(e)

fieldnames = ['version', 'rommon', 'hostname', 'uptime', 'running_image', 'hardware', 'serial']
csv_writer("./outputs/output.csv", fieldnames, BASE_PATH, "show version", "cisco_ios")
