import os
import json
import numpy as np

absPath = os.path.dirname(os.path.abspath(__file__))
needed_samples = 50
samples = []


finalTablePath = absPath + "/../../mediated-schema/final-table.json"
with open(finalTablePath, 'r') as jsonfile:
    finalTable = json.load(jsonfile)

while len(samples) < needed_samples:
    fst, snd = np.random.randint(1, len(finalTable), size=2)
    if fst != snd:
        for key in finalTable[fst]:
            if key != "" and finalTable[fst][key] == finalTable[snd][key]:
                samples.append(finalTable[fst])
                samples.append(finalTable[snd])
                break

testTablePath = absPath + "/test-table.json"
if os.path.exists(testTablePath):
    os.remove(testTablePath)
with open(testTablePath, "w") as json_file:
    json.dump(samples, json_file, indent=4)
    


