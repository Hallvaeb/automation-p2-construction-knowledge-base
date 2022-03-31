from DFABuilder import DFABuilder
from Zones.Site import Site
from Zones.Building import Building
from Zones.Storey import Storey
from Zones.Space import Space
import urllib.parse
import requests

URL = "http://127.0.0.1:3030/bot"

class Controller():

	def construct(args):
		"""
			"DEREFERENCE" ARGS AND MAKE THE CALLS NECCESSARY TO GET BUILDINGS UP.
		"""
		site_length = args[0]
		site_width = args[1]
		site_num_of_buildings = args[2]
		site_all_buildings_identical = True
		building_length = args[4]
		building_width = args[5]
		building_height = args[6]
		building_energy_consumption = args[7]
		building_number_of_storeys = args[8]
		building_all_storeys_identical = True
		space_roles = urllib.parse.unquote_plus(args[10])

		space_roles_list = str(space_roles).split(",")
		space_ids = []
		for role in space_roles_list:
			role = role.lower().strip()
			if Space.is_role_in_KB(role):
				space_id = Space([role]).get_ID()
				space_ids.append(space_id)
				print(space_id, " is what is added SPACEID HEEH")
			else:
				return "The given space role '"+str(role)+"' was not found in KB!"
		storey_id = Storey([building_length, building_width, building_height, space_ids]).get_ID()
		building_id = Building([building_length, building_width, building_height, building_energy_consumption, [storey_id]]).get_ID()
		site_id = Site([site_length, site_width, building_height, [building_id]]).get_ID()
		
		return DFABuilder.generate_DFA([[site_id], [building_id], [storey_id], space_ids])

	
	def add_space_prototype(args):
		print("add_space_prototype: " + str(args))
		length = args[0]
		width = args[1]
		height = args[2]
		energy_consumption = args[3]
		role = args[4].lower()

		space = Space([length, width, height, energy_consumption, role])
		print("add_space_prototype: " + str(args))
		space.add_to_KB()

	def send_query(query):
		params = {"query": query}
		print("PARAMS:", params)
		r = requests.get(URL, params) 
		print(r)
		if r.status_code == 404:
			return 0
		return r.json()

	def autogenerate(num_of_storeys):
		return DFABuilder.generate_DFA_with_existing_flats(num_of_storeys)