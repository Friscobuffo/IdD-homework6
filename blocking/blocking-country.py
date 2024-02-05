import country_converter as coco
import json
import os
from multiprocessing import Pool, Manager


def block_creator(args):
    entry,blocks, blocks_lock = args
    country = coco.convert(entry["Headquarter"], to='name', enforce_list=False) # Da modificare in "country"
    
    if type(country) == list:
        return 1
    else:
        with blocks_lock:
            if country in blocks:
                blocks[country].append(entry)
            else:
                blocks[country] = [entry]
        return 0    

def process_chunk(args):
    chunk, blocks, blocks_lock = args
    result = 0
    for entry in chunk:
        result += block_creator((entry, blocks, blocks_lock))
    return result

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

        results = pool.map(process_chunk, [(chunk, blocks, blocks_lock) for chunk in chunks])
    
    counter = sum(results)
    print(f"Blocks dictionary: {len(blocks)}")
    print(f"Errori nell blocking del country: {counter}")
        
if __name__ == "__main__":
    num_processes = 8
    main()

        
        
            

        
