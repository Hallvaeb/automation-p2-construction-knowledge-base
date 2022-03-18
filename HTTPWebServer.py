from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from Controller import Controller

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 4500


class ServerHandler(BaseHTTPRequestHandler):


	def do_GET(s):
		"""Respond to a GET request."""

		head = ServerHandler.create_head()
		footer = ServerHandler.create_footer()
		path = s.path

		if path.find("/") != -1 and len(path) == 1:
			
			s.send_reponse_html()

			out = head+"""<body>
					<h1>Welcome to</h1>
					<img src="/image.jpg" alt= "Logo not found." width="600" height="282">	
				<section>
						<p> This is a construction knowledge base application for creating a building
							several buildings from a set of building blocks in a knowledge base. </p>
						<a href=/add_space><button>Add Space</button></a>
						<a href=/construct_site><button>Construct!</button></a>
				</section>
			</body>
			"""+footer

			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/add_space") != -1:

			s.send_reponse_html()

			out = head + """
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Here you can add a space to the knowledge base skeleton for later use in a construction of the building.<br>
					Use the role field to specify if your space is a "flat" or a specific room or object type.<br>
					A space is, according to us, anything that can fit inside a storey of a building. <br><br>
					A good name would be: "kitchen", "bedroom" or "chair".
					</p>
				</section>
				<form action="/confirm_space" method="post">
					<fieldset>
						<legend>Space specification:</legend>
						<label for="length">Length: </label><br>
						<input type="number" name="length" id="length" value="20" ><br>
						<label for="width">Width: </label><br>
						<input type="number" name="width" id="width" value="30"><br>
						<label for="height">Height: </label><br>
						<input type="number" name="height" id="height" value="30"><br>
						<label for="energy">Energy consumption: </label><br>
						<input type="number" name="energy" id="energy" value="60000"><br>
						<label for="role">Role: </label><br>
						<input type="text" name="role" id="role" value="desk"><br>
						<div id="submit">
							<input type="submit" value="Add Space" id="submit">
						</div>
					</fieldset>
				</form>
				<a href=/><button>Go back</button></a>
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/construct_site") != -1:

			s.send_reponse_html()

			out = head + """
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Here you can create buildings automatically! <br>
					Does it require specificblocks not in the knowledge base? <br>
					Contact an engineer or add it through the 'add space' option. <br><br>
					
					<div id="license">
						License: "free version" detected: all buildings will be identical.<br>
					</div>
					</p>
				</section>
				<form action="/construct_building" method="post">
					<fieldset>
						<legend>Site specifications:</legend> 

						<label for="length">Site length [m]:</label><br>
						<input type="number" name="length" id="length" value="500"><br>

						<label for="width">Site width [m]:</label><br>
						<input type="number" name="width" id="width" value="400"> <br>

						<label for="number_of_buildings">Number of buildings: </label><br>
						<input type="number" name="number_of_buildings" id="number_of_buildings" value="5"><br>

						<label for="all_buildings_identical">Buildings identical:</label>
						<input type="checkbox" name="all_buildings_identical" onclick="return false;" checked id="all_buildings_identical" ><br>
						<div id="submit">
							<input type="submit" value="Next" id="submit">
						</div>
					</fieldset>
					</form></section>
				<a href=/><button>Cancel</button></a>
			</body>
			"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/cancel_space") != -1:

			s.send_reponse_html()
			out = head+"""
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Space cancelled! It is fully removed and erased!
					</p>
				</section>
				<a href=/add_space><button>Add space</button></a>
				<a href=/><button>Main menu</button></a>
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/image.jpg") != -1:
			
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "image/jpg")
			s.end_headers()
			try:
				# Read the file
				bReader = open("UI/automated_building_logo_scandic.jpg", "rb")
				s.wfile.write(bReader.read())
			except:
				# File not found
				print("image not found in folder")

		elif path.find("/style.css") != -1:
			
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "text/css")
			s.end_headers()
			# Read the file
			# Write file.
			bReader = open("UI/style.css", "rb")
			theImg = bReader.read()
			s.wfile.write(theImg)

		elif path.find("/favicon.ico") != -1:

			s.send_reponse_html()

			# Read the file
			# Write file.
			bReader = open("UI/favicon.ico", "rb")
			theImg = bReader.read()
			s.wfile.write(theImg)

		else:
			
			s.send_reponse_html()

			out = head+"""
			<body>
				<p>
					The path: " """ + path + """ "
					has not been implemented as a GET method.
					Start from start page!
				</p>
				<a href="/"><button>Go back</button></a>
			</body></html>"""+footer
			s.wfile.write(bytes(out, "utf-8"))

	def do_POST(s):

		head = ServerHandler.create_head()
		footer = ServerHandler.create_footer()
		path = s.path

		if path.find("/confirm_space") != -1:

			s.send_reponse_html()

			# Get the arguments
			argument_pairs = s.rfile.read(
				int(s.headers.get('Content-Length'))).decode().split("&")
			argument_list = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]

			out = head+"""
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Your space is being added... Click "OK" to confirm or CANCEL IF YOU REGRET YOUR DECISION.
					</p>
				</section>
				<section>
				<form action = "/space_added" method="post">
				<fieldset>
					<legend>Review input</legend>
					This is your input for space, you can still modify... <br>
					Lenght: 			<br><input type="Number" name="lenght" value=\""""+argument_list[0]+"""\""> <br>
					Width: 				<br><input type="Number" name="width" value=\""""+argument_list[1]+"""\"><br>
					Height: 			<br><input type="Number" name="height" value=\""""+argument_list[2]+"""\"><br>
					Energy efficiency: 	<br><input type="Number" name="energy" value=\""""+argument_list[3]+"""\"><br>
					Role: 		<br><input type="text" name="role" value=\""""+argument_list[4]+"""\"><br>
					<input id= "submit" type="submit" value="OK">
					<div id="illustration_will_appear">
								Maybe an illustration of your space will appear here some day?
					</div>
					</fieldset>
				</form>
			</section>
			<a href="/cancel_space"> <button>CANCEL</button> </a> 
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/space_added") != -1:

			s.send_reponse_html()

			# Get the arguments
			argument_pairs = s.rfile.read(
				int(s.headers.get('Content-Length'))).decode().split("&")
			args = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]

			Controller.add_space_prototype(args)

			out = head+"""
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Space added! It will now be able to appear in your construction!
					</p>
				</section>
				<a href=/add_space><button>Add another space</button></a>
				<a href=/><button>Main menu</button></a>
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/construct_building") != -1:

					s.send_reponse_html()

					# Get the arguments
					argument_pairs = s.rfile.read(
						int(s.headers.get('Content-Length'))).decode().split("&")
					args = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]
					site_length = args[0]
					site_width = args[1]
					site_num_of_buildings = args[2]
					site_all_buildings_identical = True
					# if(len(args) == 4): site_all_buildings_identical = True
					# else: site_all_buildings_identical = False
					out = head + """
					<body>
						<section>
							<h2>AUTOMATED BUILDING</h2>
							<p>
							Here you can create buildings automatically! <br>
							Does it require specific blocks not in the knowledge base? <br>
							Contact an engineer or add it through the 'add space' option.<br><br>
							
							<div id="license">
								License: "free version" detected: all storeys will be identical.<br>
							</div>
							</p>
						</section>
						<form action="/construct_storey" method="post" id="table_form">
							<input type="hidden" name="site_length" value=\""""+site_length+"""\">
							<input type="hidden" name="site_width" value=\""""+site_width+"""\">
							<input type="hidden" name="site_num_of_buildings" value=\""""+site_num_of_buildings+"""\">
							<input type="hidden" name="site_all_buildings_identical" value=\""""+str(site_all_buildings_identical)+"""\">
							<table>
								<tr>
									<th> Building Number </th>
									<th> Length [m] </th>
									<th> Width [m] </th>
									<th> Height [m] </th>
									<th> Energy Consumption [kWh]: </th>
									<th> Storeys: </th>
									<th> Storeys identical: </th>
								</tr>"""
					number_unique_buildings = 1
					if(site_all_buildings_identical):
						# all buildings identical is checked
						number_unique_buildings = 1
					else: number_unique_buildings = int(site_num_of_buildings)
					for i in range(0, number_unique_buildings):
							out += """	
								<tr>
									<td>""" + str(i+1) + """</td>
									<td><input type="number" name="length" id="length" value="40"></td>
									<td><input type="number" name="width" id="width" value="30"></td>
									<td><input type="number" name="height" id="height" value="30"></td>
									<td><input type="number" name="energy_consumption" id="energy_consumption" value="60000"></td>
									<td><input type="number" name="storeys" id='building'""" + str(i) + """ value="10"></td>
									<td><input type="checkbox" onclick="return false;" checked name="all_storeys_identical" id="all_storeys_identical"></td>
								</tr>"""
					out +="""
							</table>
							<input type="submit" value="Next" id="submit">
						</form>
						<a href=/><button>Cancel</button></a>
					</section>
					</body>
					"""+footer
					s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/construct_storey") != -1:

			s.send_reponse_html()

			# Get the arguments
			argument_pairs = s.rfile.read(
				int(s.headers.get('Content-Length'))).decode().split("&")
			args = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]
			site_length = args[0]
			site_width = args[1]
			site_num_of_buildings = args[2]
			site_all_buildings_identical = True
			building_all_storeys_identical = True

			if(site_all_buildings_identical):
				building_length = args[4]
				building_width = args[5]
				building_height = args[6]
				building_energy_consumption = args[7]
				building_number_of_storeys = args[8] 
				# building_all_storeys_identical = args[9] 
			else:
				print("ALL BUILDINGS NOT IDENTICAL IS NOT YET SUPPORTED.")

			# Declare first row header
			out = head + """
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Here you can create buildings automatically! <br>
					Does it require specific blocks not in the knowledge base? <br>
					Contact an engineer or add it through the 'add space' option.<br>
					</p>
					<div id="explanation_construct_storey">
						<p>
						Specify which spaces you'd like to have for each storey.<br>
						Must be singular form.<br>
						Examples:<br>
						1. flat<br>
						2. kitchen, bedroom, bathroom, living room<br>
						</p>
					</div>
				</section>
				<form action="/construct_construction" method="post">
					<input type="hidden" name="site_length" value=\""""+site_length+"""\">
					<input type="hidden" name="site_width" value=\""""+site_width+"""\">
					<input type="hidden" name="site_num_of_buildings" value=\""""+site_num_of_buildings+"""\">
					<input type="hidden" name="site_all_buildings_identical" value=\""""+str(site_all_buildings_identical)+"""\">
					<input type="hidden" name="building_length" value=\""""+building_length+"""\">
					<input type="hidden" name="building_width" value=\""""+building_width+"""\">
					<input type="hidden" name="building_height" value=\""""+building_height+"""\">
					<input type="hidden" name="building_energy_consumption" value=\""""+building_energy_consumption+"""\">
					<input type="hidden" name="building_number_of_storeys" value=\""""+building_number_of_storeys+"""\">
					<input type="hidden" name="building_all_storeys_identical" value=\""""+str(building_all_storeys_identical)+"""\">
					<fieldset>
					<legend> Types of spaces</legend>
					<input size="55" type="text" name="spaces" id="spaces" value="kitchen, bedroom">
					<input type="submit" value="Next" id="submit">
					</fieldset>
				</form>
				<a href=/><button>Cancel</button></a>
			</section>
			</body>
			"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/construct_construction") != -1:

			s.send_reponse_html()

			# Get the arguments
			argument_pairs = s.rfile.read(
				int(s.headers.get('Content-Length'))).decode().split("&")
			args = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]
			# Constructor.recieveFromUser
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

			[print("arg: "+ argument_pairs[i]+"\n") for i in range(len(args))]
			
			print(argument_pairs)
			out = head + """
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Congratulations! Everything is done and a construction is being created...<br>
					Wait 10 seconds for it all to load, and then press the extract solution to retrieve the OWL file for your project.<br>
					You may then upload the OWL file in NX to have your construction visualized! <br><br><br>
					Here are the arguments used (for troubleshooting pew pew): 
					</p>"""
			out += str(argument_pairs)
			out += "</section><a href=/><button>Go back</button></a></body>"+footer
			
			s.wfile.write(bytes(out, "utf-8"))

		else:
			s.send_reponse_html()

			out = head + "<body><p>The path: " + path + """ 
				has not been implemented as a POST method.
				Start from start page!</p> <a href="/"><button>Go back</button></a><br><br>
				</body></html>"""+footer

			s.wfile.write(bytes(out, "utf-8"))

	def send_reponse_html(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def create_head():
		return """
			<!DOCTYPE html>
			<HTML lang="en"> 
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<title> AUTOMATED BUILDING </title>
				<link rel="stylesheet" href="/style.css">
			</head>
			"""

	def create_footer():
		footer = """
			<footer>
				<h2 id='copyright'>©2022 AUTOMATED BUILDING</h2>
				<div id="contact_info">
					<h2>AUTOMATED BUILDING</h2>
					<h2>Verkstedteknisk, 213, Gløshaugen, Richard Birkelands vei 2b</h2>
					<h2>7034 Trondheim</h2>
					<h2>E-post: automatedbuilding@ntnu.no</h2>
				</div>
			</footer>"""
		return footer


if __name__ == '__main__':
	server_class = HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler)
	print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))

	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
