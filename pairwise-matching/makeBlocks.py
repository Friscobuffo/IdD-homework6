import os
import json
import shutil
import re

def cleanString(str):
    str = str.lower()
    return re.sub(r'[^a-zA-Z0-9]', '', str)

def makeBlocks(keys, char_num, custom_chars):
    absPath = os.path.dirname(os.path.abspath(__file__))
    
    finaTablePath = absPath + "/../mediated-schema/processed-final-table2.json"
    with open(finaTablePath, 'r') as jsonfile:
        finalTable = json.load(jsonfile)

    blocks = dict()
    for key in keys:
        for row in finalTable:
            if custom_chars:
                new_key = cleanString(row[key])[0:char_num]
            else:
                new_key = cleanString(row[key])

            if new_key not in blocks:
                blocks[new_key] = []
            blocks[new_key].append(row)
    
    print(len(blocks))
    print(max(len(block) for block in blocks.values()))

    
    if os.path.exists(absPath + "/custom-blocks"):
        shutil.rmtree(absPath + "/custom-blocks")
    os.mkdir(absPath + "/custom-blocks")

    for key in blocks.keys():
        blockPath = absPath + "/custom-blocks/%s.json" %key
        with open(blockPath, "w") as json_file:
            json.dump(blocks[key], json_file, indent=4)

def makeBlockCountry():
    makeBlocks(["country"], 0, False)

def makeBlockCompany():
    makeBlocks(["company_name"], 2, True)


if __name__ == "__main__":
    makeBlockCountry()