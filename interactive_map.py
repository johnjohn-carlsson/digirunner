from database import *
import os
from PIL import Image

def eastern_kingdoms_route(user: User, distance_ran: float):
    distance_ran = float(distance_ran) * 1000
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the 'static/images' directory and the 'usermaps' subdirectory
    static_dir = os.path.join(base_dir, 'static', 'images')
    maps_dir = os.path.join(static_dir, 'worldmaps', 'wow')
    usermaps_dir = os.path.join(static_dir, 'usermaps')

    # Ensure the usermaps directory exists
    os.makedirs(usermaps_dir, exist_ok=True)

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

    token_image_path = os.path.join(static_dir, 'tokens', user.Token)

    # Determine the checkpoint based on the distance ran
    checkpoint_distance = max([key for key in checkpoints_1.keys() if key <= distance_ran])

    # Get the corresponding coordinates for the checkpoint
    coordinates = checkpoints_1[checkpoint_distance]
    x, y = map(int, coordinates.split(','))

    # Load the map image
    map_image_path = maps["map_1"]  # You can choose the appropriate map if there are multiple
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