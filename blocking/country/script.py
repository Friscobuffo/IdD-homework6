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
            
json_file_path = os.path.join('mediated-schema', 'final-table.json') 

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)
    
chunk_size = len(data) // (8**2)
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
i = 0
for chunk in chunks:
    table_name = 'table_' + str(i) + '.json'
    json_file_path = os.path.join('blocking', 'tabels', table_name)
    blocks = chunk
    with open(json_file_path, 'w') as file:
            json.dump(blocks, file, indent=4)
    i += 1