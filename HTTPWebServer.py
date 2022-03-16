from datetime import date
import http
from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlite3 import Date
import time

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 5000


class ServerHandler(BaseHTTPRequestHandler):


	def do_GET(s):
		"""Respond to a GET request."""

		head = ServerHandler.create_head()
		footer = ServerHandler.create_footer()
		path = s.path

		if path.find("/") != -1 and len(path) == 1:
			
			s.send_reponse_html()

			out = head+"""<body>
				<section>
					<h1>Welcome to</h1>
					<h2>AUTOMATED BUILDING!</h2>
					<p> This is a construction knowledge base application for creating a building
						several buildings from a set of building blocks in a knowledge base. </p>
					<a href=/add_space><button>Add Space</button></a>
					<a href=/construct_building><button>Construct building</button></a>
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
					Use the description field to specify if your space is a "flat" or a specific room or object type.<br><br>
					A good name would be: "kitchen", "bedroom" or "chair".
					</p>
				</section>
				<form action="/space_added" method="post">
					<fieldset>
						<legend>AUTOMATED BUILDING:</legend>
						<label for="length">Length: </label><br>
						<input type="number" name="length" id="length" placeholder="length" ><br>
						<label for="width">Width: </label><br>
						<input type="number" name="width" id="width" placeholder="width"><br>
						<label for="height">Height: </label><br>
						<input type="number" name="height" id="height" placeholder="height"><br>
						<label for="description">Description: </label><br>
						<input type="String" name="description" id="description" placeholder="description"><br>
					</fieldset>
					<input type="submit" value="Add Space" id="submit">
					</form></section>
				<br><a href=/><button>Go back</button></a>
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/construct_building") != -1:

			s.send_reponse_html()

			out = head + """
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Here you can create buildings automatically! 
					Does it require specificblocks not in the knowledge base? 
					Contact an engineer or add it through the 'add space' option.
					</p>
				</section>
				<form action="/construct_storeys" method="post">
					<fieldset>
						<legend>AUTOMATED BUILDING:</legend>
						<label for="length">Site length: </label>
						<input type="number" name="length" id="length" placeholder="length" ><br>
						<label for="width">Site : </label>
						<input type="number" name="width" id="width" placeholder="width"><br>
						<label for="number_of_buildings">Number of buildings: </label>
						<input type="number" name="number_of_buildings" id="number_of_buildings" placeholder="number of buildings"><br>
						<label for="all_buildings_identical">Are all the buildings identical?: </label>
						<input type="checkbox" name="all_buildings_identical" id="all_buildings_identical"><br>
					</fieldset>
					<input type="submit" value="Next" id="submit">
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
				<a href=/add_space><button>Add another space</button></a>
				<a href=/><button>Main menu</button></a>
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/image.png") != -1:
			
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "image/png")
			s.end_headers()
			try:
				# Read the file
				bReader = open("UI/logo.png", "rb")
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
			</body></html>"""
			s.wfile.write(bytes(out, "utf-8"))

	def do_POST(s):

		head = ServerHandler.create_head()
		footer = ServerHandler.create_footer()
		path = s.path

		if path.find("/space_added") != -1:

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
				<form action = "/add_space" method="post">
					These were your inputs: <br>
					Lenght: """ + argument_list[0] + """<br>
					Width: """ + argument_list[1] + """<br>
					Height: """ + argument_list[2] + """<br>
					Description: """ + argument_list[3] + "<br>"
			# Using hidden params to pass AUTOMATED BUILDING arguments
			out += """<input type="hidden" name="lenght" value=\""""+argument_list[0]+"""\"">
					<input type="hidden" name="width" value=\""""+argument_list[1]+"""\">
					<input type="hidden" name="height" value=\""""+argument_list[2]+"""\">
					<input type="hidden" name="description" value=\""""+argument_list[3]+"""\">"""
			# Add submit button at the end and end form
			out += """<input type="submit" value="OK"></form></section>
			<a href="/cancel_space"> <button>CANCEL</button> </a> 
			</body>"""+footer
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/add_space") != -1:

			s.send_reponse_html()

			# Get the arguments
			argument_pairs = s.rfile.read(
				int(s.headers.get('Content-Length'))).decode().split("&")
			argument_list = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]

			# TODO: Call right function to add the space with the given arguments

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

		elif path.find("/construct_storeys") != -1:

			s.send_reponse_html()

			# Get the arguments
			argument_pairs = s.rfile.read(
				int(s.headers.get('Content-Length'))).decode().split("&")
			args = [argument_pairs[i].split("=")[1] for i in range(len(argument_pairs))]

			out = head + """
			<body>
				<section>
					<h2>AUTOMATED BUILDING</h2>
					<p>
					Here you can create buildings automatically! 
					Does it require specific blocks not in the knowledge base? 
					Contact an engineer or add it through the 'add space' option.
					</p>
				</section>
				<form action="/construct_spaces" method="post" id="table_form">
					<h2>AUTOMATED BUILDING</h2>
					<table>
						<tr>
							<th> Building Number: </th>
							<th> Length: </th>
							<th> Width: </th>
							<th> Height: </th>
							<th> Energy Consumption [kWh]: </th>
							<th> Storeys: </th>
							<th> All storeys in this building are identical: </th>
						</tr>"""
			no_unique_buildings = 1
			if(len(args) == 4):
				# all buildings identical is checked
				no_unique_buildings = 1
			else: no_unique_buildings = int(args[2])
			for i in range(0, no_unique_buildings):
					out += """	
						<tr>
							<td>Building """ + str(i) + """:</td>
							<td><input type="number" name="length" id="length" placeholder="Number"></td>
							<td><input type="number" name="width" id="width" placeholder="Number"></td>
							<td><input type="number" name="height" id="height" placeholder="Number"></td>
							<td><input type="number" name="energy_consumption" id="energy_consumption" placeholder="Number"></td>
							<td><input type="number" name="Storeys" id='building'""" + str(i) + """ placeholder='Number'></td>
							<td><input type="checkbox" name="all_storeys_identical" id="all_storeys_identical"></td>
						</tr>"""
			out +="""
					</table>
					<input type="submit" value="Next" id="submit">
				</form>
				<a href=/><button>Cancel</button></a>
			</section>
			</body>
			"""#+footer
			s.wfile.write(bytes(out, 'utf-8'))

		else:
			s.send_reponse_html()

			out = head + "<body><p>The path: " + path + """ 
				has not been implemented as a POST method.
				Start from start page!</p> <a href="/"><button>Go back</button></a><br><br>
				</body></html>"""

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
