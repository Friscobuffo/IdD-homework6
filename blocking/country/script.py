import json
import os
import country_converter as coco

def load_blocks():
    json_file_path = os.path.join('blocking', 'country', 'blocks_data.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_blocks(blocks):
    json_file_path = os.path.join('blocking', 'country', 'blocks_data.json')
    
    if os.path.exists(json_file_path):
        prev_blocks = load_blocks()
        for key, value in blocks.items():
            if key in prev_blocks:
                prev_blocks[key].extend(value)
 
            else:
                prev_blocks[key] = value
                
        with open(json_file_path, 'w') as file:
            json.dump(prev_blocks, file, indent=4)
    else:
        with open(json_file_path, 'w') as file:
            json.dump(blocks, file, indent=4)
            
blocks = load_blocks()
countries = []
not_found = []


for key, value in blocks.items():
    print(f"{key} : {len(value)}")


