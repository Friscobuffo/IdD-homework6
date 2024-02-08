import os
import json
import shutil

def makeBlocks(keys, char_num):
    absPath = os.path.dirname(os.path.abspath(__file__))
    
    finaTablePath = absPath + "/../mediated-schema/processed-final-table2.json"
    with open(finaTablePath, 'r') as jsonfile:
        finalTable = json.load(jsonfile)

    blocks = dict()
    for key in keys:
        for row in finalTable:
            new_key = row[key]

            if new_key not in blocks:
                blocks[new_key] = []
            blocks[new_key].append(row)
    
    print(len(blocks))

    
    if os.path.exists(absPath + "/custom-blocks"):
        shutil.rmtree(absPath + "/custom-blocks")
    os.mkdir(absPath + "/custom-blocks")

    for key in blocks.keys():
        blockPath = absPath + "/custom-blocks/%s.json" %key
        if os.path.exists(blockPath):
            os.remove(blockPath)
        with open(blockPath, "w") as json_file:
            json.dump(blocks[key], json_file, indent=4)


if __name__ == "__main__":
    makeBlocks(["country"], 2)