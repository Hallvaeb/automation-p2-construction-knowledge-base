from Zones.Site import Site
from Zones.Building import Building
from Zones.Storey import Storey
from Zones.Space import Space


class Controller():

	def construct(args):
		print(args)
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
		storey_space_roles = args[10]

		# storey_space_role_list = storey_space_roles.split("%2C+")
		storey_space_role_list = storey_space_roles.split(", ")
		print(storey_space_role_list)
		space_ids = []
		for role in storey_space_role_list:
			space_ids.append(Space(["space", role]))
		
		storey_id = Storey(["storey", building_length, building_width, building_height, space_ids])

		building_id = Building(["building", building_length, building_width, building_height, [storey_id]])

		site_id = Site(["site", site_length, site_width, building_height, [building_id]])
		

        # INPUT args: [type, length, width, height, role, adjacentZones[]]
	
	def add_space_prototype(args):
		print("add_space_prototype: " + str(args))
		length = args[0]
		width = args[1]
		height = args[2]
		energyEfficiency = args[3]
		role = args[4]

		Space([length, width, height, energyEfficiency, role])

# site_length=500
# site_width=400
# site_num_of_buildings=5
# site_all_buildings_identical=True
# building_length=40
# building_width=30
# building_height=30
# building_energy_consumption=60000
# building_number_of_storeys=10
# building_all_storeys_identical=True
# spaces="kitchen, bedroom"
# dummy_args = [site_length, site_width, site_num_of_buildings, site_all_buildings_identical, building_length, building_width, building_height, building_energy_consumption, building_number_of_storeys, building_all_storeys_identical, spaces]

# Controller.recieveFromUser(dummy_args)