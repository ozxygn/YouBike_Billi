import json
import folium
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt

# Load the instance (stations and their details)
def load_instance(instance_path):
    with open(instance_path, 'r') as f:
        instance = json.load(f)
    return instance

# Load the TSP solution (routes for multiple trucks)
def load_solution(solution_path):
    with open(solution_path, 'r') as f:
        solution = json.load(f)
    return solution['routes']  # Assuming the solution file contains a key 'routes'

# Visualize the paths on a map
def visualize_solution(instance_path, solution_path, map_output):
    instance = load_instance(instance_path)
    tsp_routes = load_solution(solution_path)

    # Convert stations to a DataFrame for easy handling
    stations = pd.DataFrame(instance['stations'])

    # Initialize a folium map centered on the first station
    first_route = tsp_routes[0]['route']
    first_station = stations.iloc[first_route[0]]
    map_center = first_station['coords'][0], first_station['coords'][1]
    mymap = folium.Map(location=map_center, zoom_start=13)
    depots_coords = [depot['coords'] for depot in instance['depots']]

    # Generate a color palette for the routes
    num_routes = len(tsp_routes)
    colormap = plt.colormaps.get_cmap('tab10')  # Get the colormap without specifying the number of colors
    route_colors = [colors.rgb2hex(colormap(i / num_routes)[:3]) for i in range(num_routes)]

    # Add the TSP paths with unique colors
    for idx, route in enumerate(tsp_routes):
        path_coordinates = [stations.iloc[i]['coords'] for i in route['route']]
        depot_id = route['depot_id']
        depot_coords = depots_coords[depot_id]
        path_coordinates.insert(0, depot_coords)
        path_coordinates.append(depot_coords)
        folium.PolyLine(
            path_coordinates, color=route_colors[idx], weight=2, opacity=1,
            tooltip=f"Route {idx + 1}"
        ).add_to(mymap)

    # Add a FeatureGroup for station markers
    marker_group = folium.FeatureGroup(name="Stations")

    # Add smaller markers to the FeatureGroup
    for _, row in stations.iterrows():
        folium.CircleMarker(
            location=row['coords'],  # Coordinates of the station
            radius=1,                # Adjust radius for smaller markers
            color="blue",            # Border color of the circle
            opacity=0.75,
            tooltip=f"Station ID: {row['id']}"  # Tooltip on hover
        ).add_to(marker_group)


    # # add the marker for the depot
    for idx, depot_coords in enumerate(depots_coords):
        folium.CircleMarker(
            location=depot_coords,  # Coordinates of the depot
            radius=2,                # Adjust radius for smaller markers
            color="red",            # Border color of the circle
            opacity=1,
            fill=True,               # Fill the circle with color
            fill_color="red",       # Fill color of the circle
            fill_opacity=1,        # Adjust transparency
            tooltip=f"Depot {idx}"  # Tooltip on hover
        ).add_to(marker_group)

    marker_group.add_to(mymap)
    folium.LayerControl().add_to(mymap)

    # Save the map to an HTML file
    mymap.save(map_output)
    print(f"Map saved as '{map_output}'")

if __name__ == "__main__":
    instance_path = "./data/instances_v4/v12-24-24_b8h_d12/NTU.json"
    solution_path = "./results/v4_cbws/NTU/NTU.json"
    save_path = solution_path.replace('.json', '.html')

    visualize_solution(instance_path, solution_path, save_path)