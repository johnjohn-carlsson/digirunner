from database import *
import os
from PIL import Image

def kalimdor_route(user: User, distance_ran: float):
    distance_ran = float(distance_ran) * 1000  # Convert to meters
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the 'static/images' directory and the 'usermaps' subdirectory
    static_dir = os.path.join(base_dir, 'static', 'images')
    maps_dir = os.path.join(static_dir, 'worldmaps', 'wow')
    usermaps_dir = os.path.join(static_dir, 'usermaps')

    # Ensure the usermaps directory exists
    os.makedirs(usermaps_dir, exist_ok=True)

    # Maps corresponding to each checkpoint dictionary
    maps = {
        "map_1": os.path.join(maps_dir, "k-1.jpg"),
        "map_2": os.path.join(maps_dir, "k-2.jpg")
    }

    # Checkpoint layouts: {"distance in meters": "XY pixel location on map"}
    checkpoints_1 = {
        0: "605,287",
        100: "622,367",
        200: "544,391",
        300: "487,343",
        400: "408,338",
        500: "340,369"
    }

    checkpoints_2 = {
        600: "359,291",
        700: "409,334",
        800: "406,398",
        900: "413,473",
        1000: "416,537",
        1100: "416,602"
    }

    # Add more checkpoint dictionaries and corresponding maps as needed
    all_checkpoints = [
        (checkpoints_1, "map_1"),
        (checkpoints_2, "map_2"),
    ]

    token_image_path = os.path.join(static_dir, 'tokens', user.Token)

    # Iterate over all checkpoint dictionaries to find the correct one and map
    checkpoint_distance = None
    coordinates = None
    map_image_path = None

    for checkpoints, map_key in all_checkpoints:
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





def eastern_kingdoms_route(user: User, distance_ran: float):
    distance_ran = float(distance_ran) * 1000  # Convert to meters
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the 'static/images' directory and the 'usermaps' subdirectory
    static_dir = os.path.join(base_dir, 'static', 'images')
    maps_dir = os.path.join(static_dir, 'worldmaps', 'wow')
    usermaps_dir = os.path.join(static_dir, 'usermaps')

    # Ensure the usermaps directory exists
    os.makedirs(usermaps_dir, exist_ok=True)

    # Maps corresponding to each checkpoint dictionary
    maps = {
        "map_1": os.path.join(maps_dir, "ek-1.jpg"),
        "map_2": os.path.join(maps_dir, "ek-2.jpg")
    }

    # Checkpoint layout: {"distance in meters": "XY pixel location on map"}
    checkpoints_1 = {
        0: "305,183",
        100: "399,210",
        200: "444,276",
        300: "468,365",
        400: "439,448",
        500: "495,532"
    }

    checkpoints_2 = {
        600: "485,91",
        700: "468,208",
        800: "436,322",
        900: "458,454"
    }

    # Add more checkpoint dictionaries and corresponding maps as needed
    all_checkpoints = [
        (checkpoints_1, "map_1"),
        (checkpoints_2, "map_2"),
    ]

    token_image_path = os.path.join(static_dir, 'tokens', user.Token)

    # Iterate over all checkpoint dictionaries to find the correct one and map
    checkpoint_distance = None
    coordinates = None
    map_image_path = None

    for checkpoints, map_key in all_checkpoints:
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