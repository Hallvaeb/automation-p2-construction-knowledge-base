from DFABuilder import DFABuilder
from Zones.Site import Site
from Zones.Building import Building
from Zones.Storey import Storey
from Zones.Space import Space
import urllib.parse

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
			role = role.lower()
			space = Space([role])
			space_ids.append(space.get_ID())
			
		storey_id = Storey([building_length, building_width, building_height, space_ids]).get_ID()
		building_id = Building([building_length, building_width, building_height, [storey_id]]).get_ID()
		site_id = Site([site_length, site_width, building_height, [building_id]]).get_ID()
		
		DFABuilder.generate_DFA([[site_id], [building_id], [storey_id], [space_ids]])

	
	def add_space_prototype(args):
		print("add_space_prototype: " + str(args))
		length = args[0]
		width = args[1]
		height = args[2]
		energyEfficiency = args[3]
		role = args[4].lower()

		space = Space([length, width, height, energyEfficiency, role])
		space.add_to_KB()

	def get_DFA(design_id):
		
		DFABuilder.make_design_template()
		DFABuilder.generate_DFA("site", 0.2, 300, 500)
		DFABuilder.generate_DFA("building", 200, 150, 300)
		DFABuilder.generate_DFA("space", 2, 11, 14)
