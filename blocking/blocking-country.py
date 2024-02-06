import country_converter as coco
import json
import os
import logging
from multiprocessing import Pool, Manager, cpu_count


def country_extractor(string):
    components = string.split(',')
    country = components[-1].strip()
    
    return country


def block_creator(args):
    entry, blocks = args
    country_raw = country_extractor(entry['country'])
    country = coco.convert(country_raw, to='name')
    print(country)
    if type(country) == list:
            if len(country) == 3 and country[2] in blocks:
               blocks[coco.convert(country[2], to='name')].append(entry)
            elif len(country) == 2 and country[1] in blocks:
               blocks[coco.convert(country[1], to='name')].append(entry)
                
    else:
        if country in blocks:
            blocks[country].append(entry)
        else:
            blocks[country] = [entry]

def process_chunk(chunk, blocks):
    
    for entry in chunk:
        block_creator((entry, blocks))
    
    
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
            print(f"***** block_data.json size: {len(prev_blocks)} *****\n")
            json.dump(prev_blocks, file, indent=4)
            file.close()
    else:
        with open(json_file_path, 'w') as file:
            json.dump(blocks, file, indent=4)
            file.close()
            

def load_blocks():
    json_file_path = os.path.join('blocking', 'country', 'blocks_data.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def main():
    coco_logger = coco.logging.getLogger()
    coco_logger.setLevel(logging.WARNING)
    
    for i in range(0, 65):
        table_name = 'table_' + str(i) + '.json'
        print(f"\n************* {table_name} **************\n")
        json_file_path = os.path.join('blocking', 'tabels', table_name) 
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        blocks = {}
        process_chunk(data, blocks)
        
        save_blocks(blocks)
        print("\nBlocks succesfully saved!")  
        json_file.close()           
        
if __name__ == "__main__":
    num_processes =  cpu_count()
    main()


        
            

        
