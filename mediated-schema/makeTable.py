import os
import json
from time import time

start = time()
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = ABS_PATH + "/valentine-ms/sources-json"

MEDIATED_SCHEMA_PATH = ABS_PATH + "/valentine-ms/mediated-schema.json"
with open(MEDIATED_SCHEMA_PATH, 'r') as jsonfile:
    mediatedSchema = json.load(jsonfile)

temp = dict()
for schema in mediatedSchema:
    name = schema.pop("dataset")
    temp[name] = schema
mediatedSchema = temp

files = os.listdir(DATA_PATH)

finalAttr = []
for schema in mediatedSchema.values():
    for value in schema.values():
        if value not in finalAttr:
            finalAttr.append(value)

finalTable = []
for file in files:
    filePath = DATA_PATH + "/" + file
    with open(filePath, 'r') as jsonfile:
        entries = json.load(jsonfile)
    keys = entries[0].keys()
    toSkip = []
    seen = []
    for newAttribute in mediatedSchema[file].values():
        if newAttribute in seen: continue
        seen.append(newAttribute)
        if list(mediatedSchema[file].values()).count(newAttribute) > 1:
            print(f"mediated schema for dateset [{file}]")
            print(f"multiple occurrence of attribute [{newAttribute}]")
            oldKeys = []
            for key in mediatedSchema[file]:
                if mediatedSchema[file][key] == newAttribute:
                    oldKeys.append(key)
                    print(f"from [{key}]")
            key = input("choose one key to use, the other one will not be used: ")
            while key not in oldKeys:
                key = input("key not valid: ")
            for k in oldKeys:
                if k != key: toSkip.append(k)
            print()

    for entry in entries:
        temp = dict()
        for attr in mediatedSchema[file]:
            if attr in toSkip: continue
            temp[mediatedSchema[file][attr]] = entry[attr]
        for attr in finalAttr:
            if attr not in temp:
                temp[attr] = ""
        finalTable.append(temp)

FINAL_TABLE_PATH = ABS_PATH + "/final-table.json"
if os.path.exists(FINAL_TABLE_PATH):
    os.remove(FINAL_TABLE_PATH)
with open(FINAL_TABLE_PATH, "w") as json_file:
    json.dump(finalTable, json_file, indent=4)

print(f"total time {time()-start}")