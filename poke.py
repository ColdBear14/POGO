import re
import math
import folium
import webbrowser

def extract_coordinates(text):
    pattern = re.compile(r'([+-]?\d+\.\d+),([+-]?\d+\.\d+)')
    return pattern.findall(text)

def haversine(coord1, coord2):
    R = 6371  
    lat1, lon1 = map(float, coord1)
    lat2, lon2 = map(float, coord2)
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

with open('data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Extract coordinates
coordinates = extract_coordinates(text)

print("Extracted coordinates:" , coordinates)

# Input coordinate from user
input_str = input("Enter coordinates (latitude,longitude): ")
input_lat, input_lon = map(float, input_str.split(','))
input_coordinate = (input_lat, input_lon)

# Calculate distances from input coordinate to each extracted coordinate
distances = []
for coord in coordinates:
    distance = haversine(input_coordinate, coord)
    distances.append((distance, coord))

# Sort distances
distances.sort()

# Create a map centered around the input coordinate
m = folium.Map(location=input_coordinate, zoom_start=5)

# Add a marker for the input coordinate
folium.Marker(location=input_coordinate, popup="Input Coordinate", icon=folium.Icon(color='red')).add_to(m)

# Add markers for each extracted coordinate
for distance, coord in distances:
    coord_float = tuple(map(float, coord))
    folium.Marker(location=coord, popup=f"Coordinate: {coord_float}, Distance: {distance:.2f} km").add_to(m)

# Save the map to an HTML file
map_file = "map.html"
m.save(map_file)

# Automatically open the map in the default web browser
webbrowser.open(map_file)

print("Coordinates and distances from input coordinate (in km) sorted by distance:")
for distance, coord in distances:
    coord_float = tuple(map(float, coord))
    print(f"Coordinate: {coord_float}, Distance: {distance:.2f} km")