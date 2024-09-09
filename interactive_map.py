from database import *
import os
from PIL import Image

def run_selected_route(user:User, distance_ran:float, world_name:str, route_name:str):

    # Create directories to work with
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, 'static', 'images')
    maps_dir = os.path.join(image_dir, 'worldmaps', world_name)
    usermaps_dir = os.path.join(image_dir, 'usermaps')
    token_image_path = os.path.join(image_dir, 'tokens', user.Token)

    # Fetch the correct map and checkpoint data for the route
    route_map, maps, route_length = fetch_map_info(route_name)

    if not route_map:
        # Handle the case where the route is not found
        return None

    checkpoint_distance = None
    coordinates = None
    map_image_path = None

    if distance_ran > route_length:
        # Make the token appear at the last checkpoint for the last map
        last_checkpoints, last_map_key = route_map[-1]  # Get the last checkpoint dictionary and map key
        checkpoint_distance = max(last_checkpoints.keys())  # Find the highest checkpoint
        coordinates = last_checkpoints[checkpoint_distance]
        map_image_path = maps[last_map_key]
    else:
        # Iterate through route_map to find the right checkpoint based on the distance
        for checkpoints, map_key in route_map:
            # Check if the current distance falls within this checkpoint's range
            if any(key <= distance_ran <= max(checkpoints.keys()) for key in checkpoints.keys()):
                checkpoint_distance = max([key for key in checkpoints.keys() if key <= distance_ran])
                coordinates = checkpoints[checkpoint_distance]
                map_image_path = maps[map_key]
                break

    if coordinates:
        x, y = map(int, coordinates.split(','))

        # Load the map image based on the selected checkpoint dictionary
        map_image = Image.open(map_image_path)

        # Load the token image
        token_image = Image.open(token_image_path).convert("RGBA")

        # Resize the token image to 40x40 pixels
        token_image = token_image.resize((40, 40), Image.LANCZOS)

        # Paste the token image onto the map at the specified coordinates
        map_image.paste(token_image, (x-20, y-20), token_image)

        # Save the resulting image to the 'usermaps' directory
        output_image_path = os.path.join(usermaps_dir, f"{user.Username}_updated_map.jpg")
        map_image.save(output_image_path)

        return output_image_path
    else:
        # Handle case where the distance ran does not match any checkpoint
        return None


def fetch_map_info(wanted_route):
    all_routes = []

    ######################################################################################
    ################################### KALIMDOR ROUTE ###################################
    ######################################################################################
    # Maps corresponding to each checkpoint dictionary
    kalimdor_maps = {
        "map_1": "static/images/worldmaps/wow/k-1.jpg",
        "map_2": "static/images/worldmaps/wow/k-2.jpg"
    }

    # Checkpoint layouts: {"distance in meters": "XY pixel location on map"}
    kalimdor_checkpoints_1 = {
        0: "605,287",
        100: "622,367",
        200: "544,391",
        300: "487,343",
        400: "408,338",
        500: "340,369"
    }

    kalimdor_checkpoints_2 = {
        600: "359,291",
        700: "409,334",
        800: "406,398",
        900: "413,473",
        1000: "416,537",
        1100: "416,602"
    }

    kalimdor_route = [
        (kalimdor_checkpoints_1, "map_1"),
        (kalimdor_checkpoints_2, "map_2"),
    ]

    total_length = 1100

    all_routes.append(("kalimdor", kalimdor_route, kalimdor_maps, total_length))

    ######################################################################################
    ############################### EASTERN KINGDOMS ROUTE ###############################
    ######################################################################################

    eastern_kingdoms_maps = {}

    for n in range(1,9):
        eastern_kingdoms_maps[f"map_{n}"] = f"static/images/worldmaps/wow/ek-{n}.jpg"

    eastern_kingdoms_checkpoints_1 = {
        0: "305,183",
        100: "399,210",
        200: "444,276",
        300: "468,365",
        400: "439,448",
        500: "495,532"
    }

    eastern_kingdoms_checkpoints_2 = {
        600: "485,91",
        700: "468,208",
        800: "436,322",
        900: "458,454"
    }

    eastern_kingdoms_checkpoints_3 = {
        1000: "539,84",
        1100: "539,147",
        1200: "530,208",
        1300: "594,293",
        1400: "583,390",
        1500: "479,452",
        1600: "369,487",
        1700: "226,487",
        1800: "116,441"    
        }
    
    eastern_kingdoms_checkpoints_4 = {
        1900: "625,362",
        2000: "525,376",
        2100: "417,391",
        2200: "316,394",
    }

    eastern_kingdoms_checkpoints_5 = {
        2300: "794,478",
        2400: "732,427",
        2500: "643,400",
        2600: "563,441",
        2700: "534,521"
    }

    eastern_kingdoms_checkpoints_6 = {
        2800: "620,69",
        2900: "543,122",
        3000: "500,214",
        3100: "529,314",
        3200: "544,414",
        3300: "560,511",
        3400: "654,528"
    }

    eastern_kingdoms_checkpoints_7 = {
        3500: "226,310",
        3600: "356,329",
        3700: "473,268",
        3800: "598,258",
        3900: "709,315",
        4000: "815,371"
    }

    eastern_kingdoms_checkpoints_8 = {
        4100: "256,312",
        4200: "358,350",
        4300: "454,399",
        4400: "446,514",
        4500: "458,612"
    }

    eastern_kingdoms_route = [
        (eastern_kingdoms_checkpoints_1, "map_1"),
        (eastern_kingdoms_checkpoints_2, "map_2"),
        (eastern_kingdoms_checkpoints_3, "map_3"),
        (eastern_kingdoms_checkpoints_4, "map_4"),
        (eastern_kingdoms_checkpoints_5, "map_5"),
        (eastern_kingdoms_checkpoints_6, "map_6"),
        (eastern_kingdoms_checkpoints_7, "map_7"),
        (eastern_kingdoms_checkpoints_8, "map_8")
    ]

    total_length = 4500

    all_routes.append(("eastern kingdoms", eastern_kingdoms_route, eastern_kingdoms_maps, total_length))

    # Match the requested route
    for route_name, route, maps, route_length in all_routes:
        if route_name == wanted_route.lower():
            return route, maps, route_length
    return None, None
