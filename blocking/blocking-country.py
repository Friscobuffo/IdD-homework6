import country_converter as coco
import json
import os
from multiprocessing import Pool, Manager, cpu_count


def block_creator(args):
    entry,blocks, blocks_lock = args
    country = coco.convert(entry["Headquarter"], to='name', enforce_list=False) # Da modificare in "country"

    if type(country) == list:
        with blocks_lock:
                if len(country) == 3 and country[2] in blocks:
                    blocks[coco.convert(country[2], to='name')].append(entry)
                elif len(country) == 2 and country[1] in blocks:
                    blocks[coco.convert(country[1], to='name')].append(entry)
                
    else:
        with blocks_lock:
            if country in blocks:
                blocks[country].append(entry)
            else:
                blocks[country] = [entry]

def process_chunk(args):
    chunk, blocks, blocks_lock = args
    for entry in chunk:
        block_creator((entry, blocks, blocks_lock))

def main():
    with Pool(processes=num_processes) as pool:
        json_file_path = os.path.join('sources-json', 'MarScoToc-ambitionbox.com.json')

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        chunk_size = len(data) // num_processes
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        manager = Manager()
        blocks = manager.dict()
        blocks_lock = manager.Lock()

        pool.map(process_chunk, [(chunk, blocks, blocks_lock) for chunk in chunks])

    # merged_values = blocks["United States"] + blocks["United States Virgin Islands"]
    # del blocks["United States"]
    # del blocks["United States Virgin Islands"]
    # blocks["United States"] = merged_values

        
if __name__ == "__main__":
    num_processes =  2 #cpu_count()
    main()

      
        
            

        
