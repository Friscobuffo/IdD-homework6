import country_converter as coco
import json
import os


def block_creator(entry, blocks, counter):
    
    country = coco.convert(entry["Headquarter"], to='name', enforce_list=False)
    if type(country) == list:
        counter += 1
    else:
        if country in blocks:
            blocks[country].append(entry)
        else:
            blocks[country] = [entry]

    return counter


blocks = {}
counter = 0
json_file_path = os.path.join('sources-json', 'MarScoToc-ambitionbox.com.json') # Prova

with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        for entry in data:
            counter = block_creator(entry, blocks, counter)
print(blocks)

    
    
        

    
