import json
import os.path

import configs


def read_path_json(path = configs.get_proj_path()):
    print(">>>",path)
    try:
        with open(os.path.join(path,"pages","pages.json"), 'r') as file:
            json_data = json.load(file)
            return json_data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
