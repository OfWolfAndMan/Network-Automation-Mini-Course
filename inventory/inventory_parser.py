from ntc_templates.parse import parse_output
import os
import csv

BASE_PATH = "./config/"

with open("./output/output.csv", 'w', newline='\n') as csvfile:
	fieldnames = ['version', 'rommon', 'hostname', 'uptime', 'running_image', 'hardware', 'serial']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for file in os.listdir(BASE_PATH):
		file = open(BASE_PATH + file)
		config = file.read()
		inventory_parsed = parse_output(platform="cisco_ios", command="show version", data=config)
		inv_fixed = {k: v for k, v in inventory_parsed[0].items() if k in fieldnames}
		writer.writerow(inv_fixed)
