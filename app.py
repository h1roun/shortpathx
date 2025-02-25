from flask import Flask, render_template, request, jsonify
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import folium
import os
import json
import numpy as np

# Set the OSMnx cache directory
ox.settings.cache_folder = os.path.join(os.path.dirname(__file__), 'cache')
ox.settings.use_cache = True

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize geocoder
geolocator = Nominatim(user_agent="algeria_router")

# Load Algeria graph once at startup
algeria_graph = None
try:
    algeria_graph = ox.load_graphml('algeria_graph.graphml')
except:
    print("Downloading Algeria network data, this may take some time...")
    algeria_graph = ox.graph_from_place('Algeria', network_type='drive')
    ox.save_graphml(algeria_graph, 'algeria_graph.graphml')

# Default coordinates for Bejaia
BEJAIA_COORDS = (36.7528, 5.0567)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_route', methods=['POST'])
def get_route():
    data = request.get_json()
    origin = data.get('origin', 'Bejaia, Algeria')
    destination = data.get('destination')
    
    if not destination:
        return jsonify({"error": "Destination is required"}), 400
    
    try:
        # Geocode origin and destination
        origin_location = geolocator.geocode(origin)
        dest_location = geolocator.geocode(f"{destination}, Algeria")
        
        if not origin_location or not dest_location:
            return jsonify({"error": "Could not geocode one of the locations"}), 400
        
        origin_point = (origin_location.latitude, origin_location.longitude)
        dest_point = (dest_location.latitude, dest_location.longitude)
        
        # Find nearest network nodes
        origin_node = ox.distance.nearest_nodes(algeria_graph, origin_point[1], origin_point[0])
        dest_node = ox.distance.nearest_nodes(algeria_graph, dest_point[1], dest_point[0])
        
        # Calculate shortest path
        route = nx.shortest_path(algeria_graph, origin_node, dest_node, weight='length')
        
        # Get route coordinates
        route_coords = []
        for node in route:
            y = algeria_graph.nodes[node]['y']
            x = algeria_graph.nodes[node]['x']
            route_coords.append([y, x])
        
        # Calculate route stats
        route_length = int(ox.utils_graph.get_route_edge_attributes(algeria_graph, route, 'length').sum())
        
        # Create a map
        m = folium.Map(location=[origin_point[0], origin_point[1]], zoom_start=7)
        
        # Add markers for origin and destination
        folium.Marker(
            origin_point, 
            popup=origin, 
            icon=folium.Icon(color='green', icon='play')
        ).add_to(m)
        
        folium.Marker(
            dest_point, 
            popup=destination, 
            icon=folium.Icon(color='red', icon='flag')
        ).add_to(m)
        
        # Add route line
        folium.PolyLine(
            route_coords, 
            color="blue", 
            weight=5, 
            opacity=0.75, 
            tooltip=f"Distance: {route_length/1000:.1f} km"
        ).add_to(m)
        
        # Save map to HTML string
        map_html = m._repr_html_()
        
        return jsonify({
            "map_html": map_html,
            "distance": f"{route_length/1000:.1f} km",
            "origin": {
                "name": origin,
                "coordinates": origin_point
            },
            "destination": {
                "name": destination,
                "coordinates": dest_point
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/popular_destinations')
def popular_destinations():
    # Some popular destinations in Algeria
    destinations = [
        {"name": "Algiers", "description": "The capital city of Algeria"},
        {"name": "Oran", "description": "Major port city in the northwest"},
        {"name": "Constantine", "description": "City of bridges in northeastern Algeria"},
        {"name": "Annaba", "description": "Coastal city in northeastern Algeria"},
        {"name": "Tlemcen", "description": "City in northwestern Algeria"},
        {"name": "Ghardaïa", "description": "City in central northern Algeria"},
        {"name": "Sétif", "description": "City in northeastern Algeria"},
        {"name": "Tamanrasset", "description": "Major city in southern Algeria"}
    ]
    return jsonify(destinations)

if __name__ == '__main__':
    app.run(debug=True)
