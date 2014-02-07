import requests
import json
from datetime import datetime

def get_settings(param_file_name):
	"""Get parameters"""
	param_file = open(param_file_name, 'r')
	output = json.loads(param_file.read())
	param_file.close()
	return output

def params(param_keys):
	"""Generates parameters for query"""
	origin = param_keys['origin']
	destination = param_keys['destination']
	sensor = param_keys['sensor']
	param_text = 'origin={}&destination={}&sensor={}'
	return param_text.format(origin, destination, sensor)

def duration(param_keys):
	"""Returns the duration (in seconds) to location"""
	url = 'http://maps.googleapis.com/maps/api/directions/json?'
	request_url = url + params(param_keys)
	directions = json.loads(requests.get(request_url).content)
	return directions['routes'][0]['legs'][0]['duration']['value']

def write_to_db(output_file_name, param_file_name):
	"""Gets data and writes to db"""
	param_keys = get_settings(param_file_name)
	time_info = str(datetime.now())
	duration_info = duration(param_keys)
	output_file = open(output_file_name, 'a')
	output_file.write('{}\t{}\n'.format(time_info, duration_info))
	output_file.close()

write_to_db('duration_db.txt', 'gmaps_params.txt')