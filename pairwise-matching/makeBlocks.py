import os
import json



def makeBlocks(keys, char_num):
    absPath = os.path.dirname(os.path.abspath(__file__))
    
    finaTablePath = absPath + "/../mediated-schema/final-table.json"
    with open(finaTablePath, 'r') as jsonfile:
        finalTable = json.load(jsonfile)

    blocks = dict()
    for key in keys:
        for row in finalTable:
            new_key = row[key][0:char_num]

            if new_key not in blocks:
                blocks[new_key] = []
            blocks[new_key].append(row)
    
    print(len(blocks))

    for key in blocks.keys():
        blockPath = absPath + "/custom-blocks/%s.json" %key
        if os.path.exists(blockPath):
            os.remove(blockPath)
        with open(blockPath, "w") as json_file:
            json.dump(blocks[key], json_file, indent=4)




if __name__ == "__main__":
    makeBlocks(["company_name"], 2)