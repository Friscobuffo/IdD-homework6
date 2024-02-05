import os
import pickle
import shutil
import json

absPath = os.path.dirname(os.path.abspath(__file__))
MATCHES_DIRECTORY = absPath + "/matches"
allMatches = os.listdir(MATCHES_DIRECTORY)
matches = dict()
for fileName in allMatches:
    filePath = MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'rb') as pickleFile:
        m = pickle.load(pickleFile)
    for key in m:
        score = m[key]
        if score>0.3: matches[key] = score
sets = []
for key in matches:
    dataset0 = key[0]
    dataset1 = key[1]
    combined = set()
    combined.add(dataset0)
    combined.add(dataset1)
    j = 0
    for s in sets:
        if dataset0 in s:
            temp = sets.pop(j)
            combined = combined.union(temp)
        j += 1
    j = 0
    for s in sets:
        if dataset0 in s:
            temp = sets.pop(j)
            combined = combined.union(temp)
        j += 1
    sets.append(combined)

absPath = os.path.dirname(os.path.abspath(__file__))
PROCESSED_MATCHES_DIRECTORY = absPath + "/processed-matches"
if os.path.exists(PROCESSED_MATCHES_DIRECTORY):
    shutil.rmtree(PROCESSED_MATCHES_DIRECTORY)
os.mkdir(PROCESSED_MATCHES_DIRECTORY)
for i, s in enumerate(sets):
    fileName = "matches"+str(i)+".txt"
    filePath = PROCESSED_MATCHES_DIRECTORY + "/" + fileName
    with open(filePath, 'w') as f:
        for elem in s:
            f.write(str(elem) + '\n')

labelsMediatedSchema = []
for s in sets:
    print(s)
    print("what name do you want to give to this set of attibutes?")
    name = input()
    print()
    labelsMediatedSchema.append(name)

SOURCES_DIRECTORY = absPath + "/sources-json"
files = os.listdir(SOURCES_DIRECTORY)
schemas = []
for file in files:
    filePath = SOURCES_DIRECTORY + "/" + file
    with open(filePath, 'r') as jsonfile:
        data = json.load(jsonfile)[0]
    for key in data:
        label = None
        for i, s in enumerate(sets):
            for elem in s:
                dataset = elem[0]
                column = elem[1]
                if dataset != file: continue
                if key != column: continue
                label = labelsMediatedSchema[i]
                break
            if label: break
        if not label:
            print(f"{key} from {file} needs a label, input wanted label:")
            label = input()
        data[key] = label
    data["dataset"] = file
    schemas.append(data)

mediatedSchemaPath = absPath + "/mediated-schema.json"
if os.path.exists(mediatedSchemaPath):
    os.remove(mediatedSchemaPath)
with open(mediatedSchemaPath, "w") as json_file:
    json.dump(schemas, json_file, indent=4)