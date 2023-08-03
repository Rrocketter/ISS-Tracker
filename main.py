import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder


url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())
file = open("iss.txt", "w")
file.write("There are currently " + str(result["number"]) + " astronauts in space: \n\n ")
people = result["people"]
for p in people:
    file.write(p["name"] + "is on board the " + p["craft"] + "\n")

#print longitude and latitude
g = geocoder.ip('me')
file.write("\n Your current latitude / longitude is: " + str(g.latlng))
file.close()
webbrowser.open("iss.txt")

#the world map in turtle module
screen = turtle.Screen()
screen.setup(1200, 605)
screen.setworldcoordinates(-180, -90, 180, 90)

#load map image
screen.bgpic("map.gif")
screen.register_shape("iss.gif")
iss = turtle.Turtle()
iss.shape("iss.gif")
iss.setheading(45)
iss.penup()

iss_positions = []

while True:
    #load the current status of the ISS live
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    #extract iss location
    location = result["iss_position"]
    iss_latitude = location['latitude']
    iss_longitude = location['longitude']

    #output lat & long to terminal
    iss_latitude = float(iss_latitude)
    iss_longitude = float(iss_longitude)
    print("\nLatitude: " + str(iss_latitude))
    print("\nLongitude: " + str(iss_longitude))

    #update iss icon on map
    iss.goto(iss_longitude, iss_latitude)

    # Add the current ISS latitude and longitude to the iss_positions list
    iss_positions.append((iss_longitude, iss_latitude))

    # Draw the red line representing the projected path of the ISS
    iss.penup()
    iss.pencolor("red")
    for pos in iss_positions:
        iss.goto(pos)
    iss.pendown()

    # Refresh position every 5 seconds
    time.sleep(5)
